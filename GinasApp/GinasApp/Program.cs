using GinasApp.Data;
using GinasApp.Services;
using GinasApp.Services.Interfaces;
using MudBlazor.Services;
using Syncfusion.Blazor;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSingleton<WeatherForecastService>();
builder.Services.AddScoped<IGptService, GptService>();
builder.Services.AddSyncfusionBlazor();
builder.Services.AddMudServices();
builder.Services.AddHttpClient("api", 
    (provider, client) => client.BaseAddress = new Uri(builder.Configuration["Api"]));

var app = builder.Build();
Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense(app.Configuration["SyncfusionKey"]);

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();

app.UseRouting();

app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
