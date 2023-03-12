using System;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using dotenv.net;

namespace BestPal
{
    class Program
    {   
        private static SpeechConfig speechConfig;
        static async Task Main(string[] args)
        {
            IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
            IConfigurationRoot configuration = builder.Build();
            string cogKey = configuration["CognitiveServiceKey"];
            string cogRegion = configuration["CognitiveServiceRegion"];
            string openaiKey = configuration["OpenAIKey"];

            // Configure speech service
            var speechConfig = SpeechConfig.FromSubscription(cogKey, cogRegion);

            // Configure speech synthesis
            speechConfig.SpeechSynthesisVoiceName = "en-GB-LibbyNeural";
            var synthesizer = new SpeechSynthesizer(speechConfig);

            // Configure OpenAI
            OpenAI.Authentication = openaiKey;

            while (true)
            {
                try
                {
                    // Get spoken input
                    var command = await TranscribeCommand(speechConfig);

                    // Handle no input
                    if (string.IsNullOrEmpty(command))
                    {
                        Console.WriteLine("Waiting 2 seconds...");
                        Thread.Sleep(2000);
                        continue;
                    }

                    // Handle quit
                    if (command.ToLower() == "quit")
                    {
                        break;
                    }

                    // Handle time case (specific phrase)
                    if (command.ToLower() == "what time is it?")
                    {
                        var now = DateTime.Now;
                        var readAloudText = $"The time is {now.Hour}:{now.Minute:00}";
                        await ReadAloud(readAloudText, synthesizer);
                    }

                    // Handle general case
                    else
                    {
                        var answer = await CallOpenAI(command.ToLower());
                        await ReadAloud(answer, synthesizer);
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }

        static async Task<string> TranscribeCommand(SpeechConfig speechConfig)
        {
            var result = await new SpeechRecognizer(speechConfig, AudioConfig.FromDefaultMicrophoneInput()).RecognizeOnceAsync();
            return result.Reason == ResultReason.RecognizedSpeech ? result.Text : string.Empty;
        }

        static async Task<string> CallOpenAI(string command)
        {
            // Query OpenAI
            var response = await OpenAI.Completions.Create(
                model: "text-davinci-003",
                prompt: command,
                temperature: 0.9,
                maxTokens: 500,
                topP: 1,
                frequencyPenalty: 0,
                presencePenalty: 0.6
            );

            // Print and read aloud answer from OpenAI
            var answer = response.Choices.First().Text;
            return answer;
        }

        static async Task ReadAloud(string text, SpeechSynthesizer synthesizer)
        {
            // Print the response
            Console.WriteLine(text);

            // Synthesize spoken output
            var result = await synthesizer.SpeakSsmlAsync($"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-GB-LibbyNeural'>{text}</voice></speak>");
            if (result.Reason != ResultReason.SynthesizingAudioCompleted)
            {
                Console.WriteLine(result.Reason);
            }
        }
    }
}
