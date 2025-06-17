namespace KinectPosturaAPI.Models
{
    public class Sesion
    {
        public int Id { get; set; }
        public string UserId { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }

        public float LeftElbow { get; set; }
        public float RightElbow { get; set; }
        public float LeftKnee { get; set; }
        public float RightKnee { get; set; }

        public string Prediccion { get; set; } = string.Empty;
    }
}
