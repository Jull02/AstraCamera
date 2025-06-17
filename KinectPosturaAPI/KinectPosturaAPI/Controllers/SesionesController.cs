using Microsoft.AspNetCore.Mvc;
using KinectPosturaAPI.Models;
using System.Collections.Generic;
using System.Linq;

namespace KinectPosturaAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SesionesController : ControllerBase
    {
        // Simulación de almacenamiento en memoria
        private static readonly List<Sesion> sesiones = new();

        [HttpPost]
        public IActionResult RegistrarSesion([FromBody] Sesion sesion)
        {
            sesiones.Add(sesion);
            Console.WriteLine($"📥 Sesión registrada: {sesion.UserId}, {sesion.Timestamp}, predicción: {sesion.Prediccion}");
            return Ok(new
            {
                mensaje = "Sesión registrada correctamente (simulado)",
                datos = sesion
            });
        }

        [HttpGet]
        public IActionResult ObtenerSesiones([FromQuery] string userId)
        {
            if (string.IsNullOrEmpty(userId))
                return BadRequest("Debe proporcionar un userId");

            var resultados = sesiones
                .Where(s => s.UserId == userId)
                .OrderByDescending(s => s.Timestamp)
                .ToList();

            return Ok(resultados);
        }
    }
}
