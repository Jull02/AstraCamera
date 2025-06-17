using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Agregar servicios necesarios
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Habilitar CORS para permitir llamadas desde el frontend
builder.Services.AddCors();

var app = builder.Build();

// Configuración del middleware
app.UseSwagger();
app.UseSwaggerUI();

// Habilitar CORS para todas las solicitudes
app.UseCors(policy =>
    policy.AllowAnyOrigin()
          .AllowAnyMethod()
          .AllowAnyHeader()
);

app.UseAuthorization();

// Mapear los controladores
app.MapControllers();

app.Run();
