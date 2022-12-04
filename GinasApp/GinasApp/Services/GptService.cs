using System.Net.Http.Headers;
using GinasApp.Data;
using GinasApp.Services.Interfaces;
using Newtonsoft.Json;

namespace GinasApp.Services;

public class GptService : IGptService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly Random _random = new();

    public GptService(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public async Task<ExplanatoryResponse?> GetExplanatoryAsync(string userId, string sessionId, ExplanatoryRequest explanatoryRequest)
    {
        var content = JsonConvert.SerializeObject(explanatoryRequest);
        var response = await SendPost<ExplanatoryResponse>(userId, sessionId, "get_explanation", content);
        return response;
    }

    public async Task<AnswerResponse> GetAnswerAsync(string userId, string sessionId, AnswerRequest answerRequest)
    {
        var content = JsonConvert.SerializeObject(answerRequest);
        var response = await SendPost<AnswerResponse>(userId, sessionId, "get_answer", content);
        return response;
    }
    private async Task<T?> SendPost<T>(string userId, string sessionId, string action, string content)
    {
        try
        {
            var httpClient = _httpClientFactory.CreateClient("api");

            httpClient.DefaultRequestHeaders.Add("user-id", userId);
            httpClient.DefaultRequestHeaders.Add("session-id", sessionId);

            var response = await httpClient.PostAsync(action, 
                new StringContent(content, new MediaTypeWithQualityHeaderValue("application/json")));
            var stringContent = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<T>(stringContent);
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            return default;
        }
    }
}