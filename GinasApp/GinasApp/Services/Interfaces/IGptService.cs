using GinasApp.Data;

namespace GinasApp.Services.Interfaces;

public interface IGptService
{
    Task<ExplanatoryResponse?> GetExplanatoryAsync(string userId, string sessionId, ExplanatoryRequest explanatoryRequest);

    Task<AnswerResponse> GetAnswerAsync(string userId, string sessionId, AnswerRequest answerRequest);
}