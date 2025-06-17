using Microsoft.Azure.Kinect.Sensor;
using Microsoft.Azure.Kinect.BodyTracking;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Numerics;
using System.Runtime.InteropServices;

namespace KinectJointService.Services
{
    public static class KinectManager
    {
        private static Device device;
        private static Tracker tracker;
        private static Calibration calibration;
        private static Skeleton lastSkeleton;
        private static byte[] lastImage;

        private static bool isRunning = false;

        public static void Start()
        {
            if (isRunning) return;

            device = Device.Open(0);
            calibration = device.GetCalibration();

            device.StartCameras(new DeviceConfiguration
            {
                ColorFormat = Microsoft.Azure.Kinect.Sensor.ImageFormat.ColorBGRA32, // Fully qualified name to resolve ambiguity  
                ColorResolution = ColorResolution.R720p,
                DepthMode = DepthMode.NFOV_Unbinned,
                SynchronizedImagesOnly = true,
                CameraFPS = FPS.FPS30
            });

            tracker = Tracker.Create(calibration, new TrackerConfiguration
            {
                ProcessingMode = TrackerProcessingMode.Gpu,
                SensorOrientation = SensorOrientation.Default
            });

            isRunning = true;
        }

        public static void Stop()
        {
            if (!isRunning) return;

            tracker.Dispose();
            device.Dispose();
            isRunning = false;
        }

        public static Skeleton GetLatestSkeleton()
        {
            return lastSkeleton;
        }

        public static byte[] GetLatestImage()
        {
            return lastImage;
        }

        public static void UpdateFrame()
        {
            if (!isRunning) return;

            using var capture = device.GetCapture();
            tracker.EnqueueCapture(capture);

            using var frame = tracker.PopResult();
            if (frame == null || frame.NumberOfBodies == 0) return;

            lastSkeleton = frame.GetBody(0).Skeleton;
            lastImage = ExtractImage(capture.Color);
        }

        private static byte[] ExtractImage(Microsoft.Azure.Kinect.Sensor.Image colorImage)
        {
            byte[] raw = new byte[colorImage.Size];
            Marshal.Copy(colorImage.Memory.ToArray(), 0, Marshal.UnsafeAddrOfPinnedArrayElement(raw, 0), raw.Length); // Fix: Convert Memory to array and use UnsafeAddrOfPinnedArrayElement for IntPtr  

            using var bitmap = new Bitmap(colorImage.WidthPixels, colorImage.HeightPixels, PixelFormat.Format32bppArgb);
            var data = bitmap.LockBits(
                new Rectangle(0, 0, bitmap.Width, bitmap.Height),
                ImageLockMode.WriteOnly,
                bitmap.PixelFormat);

            try
            {
                unsafe
                {
                    fixed (byte* rawPtr = raw)
                    {
                        byte* source = rawPtr;
                        byte* dest = (byte*)data.Scan0;

                        for (int y = 0; y < colorImage.HeightPixels; y++)
                        {
                            Buffer.MemoryCopy(
                                source + (y * colorImage.StrideBytes),
                                dest + (y * data.Stride),
                                data.Stride,
                                colorImage.WidthPixels * 4);
                        }
                    }
                }
            }
            finally
            {
                bitmap.UnlockBits(data);
            }

            using var ms = new MemoryStream();
            bitmap.Save(ms, System.Drawing.Imaging.ImageFormat.Jpeg); // Fix: Fully qualify 'ImageFormat' to resolve ambiguity  
            return ms.ToArray();
        }

        public static PointF? ProjectJointToColor(Joint joint)
        {
            var pos3D = new Vector3(joint.Position.X, joint.Position.Y, joint.Position.Z);
            var result = calibration.TransformTo2D(pos3D, CalibrationDeviceType.Depth, CalibrationDeviceType.Color);
            return result.HasValue ? new PointF(result.Value.X, result.Value.Y) : null;
        }
    }
}
