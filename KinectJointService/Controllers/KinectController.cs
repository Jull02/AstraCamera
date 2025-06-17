using Microsoft.AspNetCore.Mvc;
using KinectJointService.Services;

namespace KinectJointService.Controllers
{
    [ApiController]
    [Route("api/kinect")]
    public class KinectController : ControllerBase
    {
        [HttpPost("start")]
        public IActionResult Start() { KinectManager.Start(); return Ok("Kinect started"); }

        [HttpPost("stop")]
        public IActionResult Stop() { KinectManager.Stop(); return Ok("Kinect stopped"); }
    }
}
