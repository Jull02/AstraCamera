using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Kinect.Sensor;
using KinectJointService.Services;
using System.Drawing;
using System.Drawing.Imaging;
using System.Collections.Generic;
using System.Numerics;
using Microsoft.Azure.Kinect.BodyTracking;
using System;

namespace KinectJointService.Controllers
{
    [ApiController]
    [Route("api/joints")]
    public class JointsController : ControllerBase
    {
        [HttpGet("live")]
        public IActionResult GetLive()
        {
            var skeleton = KinectManager.GetLatestSkeleton();
            if (skeleton.Equals(default(Skeleton))) // Fix: Compare with default(Skeleton) instead of null
                return NotFound("No bodies detected");

            var joints = new Dictionary<string, object>();
            foreach (JointId id in Enum.GetValues(typeof(JointId)))
            {
                var joint = skeleton.GetJoint(id);
                joints[id.ToString()] = new
                {
                    X = joint.Position.X / 1000.0,
                    Y = joint.Position.Y / 1000.0,
                    Z = joint.Position.Z / 1000.0
                };
            }
            return Ok(joints);
        }

        [HttpGet("render")]
        public IActionResult GetRender()
        {
            var skeleton = KinectManager.GetLatestSkeleton();
            var imageData = KinectManager.GetLatestImage();
            if (skeleton.Equals(default(Skeleton)) || imageData == null) // Fix: Compare skeleton with default(Skeleton)
                return NotFound("No bodies detected");

            // Se podría dibujar encima, pero si deseas solo la imagen original con esqueleto ya renderizado desde Python, puedes omitir esta parte.
            return File(imageData, "image/jpeg");
        }
    }
}
