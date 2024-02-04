import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { preview } from "../assets";
import { getRandomPrompt } from "../utils";
import { FormFields, Loader } from "../components";
import FileUpload from "../components/FileUpload";
import { africa1 } from "../assets/index";
import ChatPage from "./ChatPage";

const CreatePost = () => {
    const navigate = useNavigate();
    const models_list = [
        {"model_name": "Llama2 Model",
        "model_type": ""
    },
    {"model_name": "Finetuned Llama2 Model",
    "model_type": ""
    },
    {"model_name": "GPT 3.5 TURBO Model",
    "model_type": "gpt-3.5-turbo"
    },
    {"model_name": "GPT 4.0 Model",
    "model_type": "gpt-4-1106-preview"
    }
    ]
    const [selectedModel, setSelectedModel] = useState(models_list[0].model_name); // Set the default selected model
    console.log(selectedModel)
    const [message, setMessage] = useState('');
    const [chatResponse, setchatResponse] = useState('');

    console.log("selectedModel create page: ", selectedModel)


    const submitQuery= async () => {
        if (form.scenario) {
            try {
                setGeneratingprompt(true);
                const response = await fetch(
                    "https://192.168.137.236/api/generate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            prompt: form.scenario,
                        }),
                    }
                );
                const data = await response.json();
                setForm({ ...form, preview: `data:image/jpeg;base64,${data.photo}` });
                setResult(data.result); // Set the result in the state
            } catch (err) {
                console.log(err);
            } finally {
                setGeneratingprompt(false);
            }
        } else {
            alert("Please provide a proper prompt");
        }
    };

    const handleMessageChange = (event) => {
        setMessage(event.target.value);
    };

    console.log('Submitted input:', message);
    console.log('Submitted input:', chatResponse);

    const submitInput = async () => {
        // Handle submitting the input, you can use the 'message' state here
        // Add your logic for submitting the input to the backend
        try {
        const response = await fetch(
            'https://9bba-196-189-127-38.ngrok-free.app/api/v1/chat', {

            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "message":message , "model_type":models_list[selectedModel].model_type}),
        });

        if (response.ok) {
            
            setMessage('')
            setchatResponse(response);
        } else {
            console.error('Failed to submit input to the backend');
        }
        } catch (error) {
        console.error('Error during API call:', error);
        }
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (form.scenario && form.preview) {
            setLoading(true);
            try {
                const response = await fetch(
                    "https://192.168.137.236/api/generate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ ...form}),
                    }
                );
    
                if (response.ok) {
                    const responseData = await response.json();
                    // Assuming the response has a property named "result"
                    const result = responseData.result;
    
                    // Do something with the result
                    console.log(result);
                    // You can also update your UI or state with the received result
                } else {
                    console.log("Failed to get a successful response from the server");
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        } else {
            alert("Please generate a prompt with proper details");
        }
    };
    
    return (
        <section className="flex flex-row bg-white min-h-[calc(100vh)]">
                <div className="sm:hidden  md:flex md:flex-col md:w-1/3 md:flex-shrink-0 md:lg:w-[240px] md:h-[calc(100vh-120px)] md:whitespace-nowrap md:fixed bg-white md:overflow-x-hidden md:transition-all md:ease-in-out pt-2">
                    <div className="flex flex-col mt-24 items-start space-y-4  md:h-full ml-[16px]">
                        <label className="text-lg ml-4 font-bold text-black" id="demo-radio-buttons-group-label">
                            Select Model
                        </label>

                        <div className="flex flex-col space-y-2 pl-2 items-start">
      {models_list.map((model, index) => (
        <div key={index}>
          <input
            type="radio"
            id={`model-${index}`}
            name="radio-buttons-group"
            value={model.model_name}
            className="mr-2"
            checked={index === selectedModel}
            onChange={() => setSelectedModel(index)}
          />
          <label htmlFor={`model-${index}`} className="text-base text-black">
            {model.model_name}
          </label>
        </div>
      ))}
      
    </div>
                    </div>
                </div>
  {/* Main Content */}
                <div className="flex flex-col h-full md:w-3/4 px-4 py-6 sm:w-full">
                    {/* <div className="sm:flex sm:flex-col md:ml-[530px]  sm:ml-[100px] sm:mt-16 sm:font-extrabold sm:text-text sm:text-[42px]">
                        <h1 className="md:ml-[100px] text-black sm:text-[40px] sm:ml-[160px]">አድባር</h1>

                        <div className="flex justify-center space-x-6 mt-8 ml-[-4px]">

                            <div className="md:text-3xl text-xl text-black bg-gray-100 rounded-lg p-6 shadow-md sm:max-w-[400px] md:max-w-[1600px]">
                                <h2 className="font-bold ml-4">Retail</h2>
                                <p className="text-gray-600">Generate Telegram Ad</p>
                            </div>

                            <div className="md:text-3xl text-xl text-black bg-gray-100 rounded-lg p-6 shadow-md sm:max-w-[400px] md:max-w-[1600px]">
                                <h2 className="font-bold ml-4">Automotive</h2>
                                <p className="text-gray-600">Generate Telegram Ad</p>
                            </div>

                            <div className="md:text-3xl text-xl text-black bg-gray-100 rounded-lg p-6 shadow-md sm:max-w-[400px] md:max-w-[1600px]">
                                <h2 className="font-bold ml-4">Real Estate</h2>
                                <p className="text-gray-600">Generate Telegram Ad</p>
                            </div>
                            </div>
                </div> */}

                    <ChatPage selectedModel={selectedModel} />
                    
{/* 
                    <div className="sm:flex sm:flex-col md:ml-32 sm:ml-[-40px] sm:w-3/4">

                        <footer className="flex-row-2 mt-2 mb-2 border-blue-800 p-4 absolute bottom-0 ml-36 w-3/4" onSubmit={handleSubmit}>
                        <label for="chat" class="sr-only">Your message</label>
                            <div class="flex items-center py-2 px-3 bg-blue-800 rounded-lg dark:bg-blue-800">
                            <FileUpload/>
                            <div>

    
                                <textarea
                                    id="chat" 
                                    rows="1" 
                                    
                                    class="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border focus:ring-blue-500 focus:border-blue-500 dark:bg-white-800 dark:border-blue-800 dark:placeholder-blue-800 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                    placeholder="Your message..."
                                    value={message}
                                    onChange={handleMessageChange}
                                />
      

                                <button
                                    type="submit"
                                    onClick={submitInput}
                                    class="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600">
                                    <svg
                                    className="w-6 h-6 rotate-90"
                                    fill="white"
                                    viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg"
                                    >
                                    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
                                    </svg>
                                </button>
                            </div>

    {chatResponse && (
        <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }} className="mt-[30px]">
          <p>Response:</p>
          <pre>{JSON.stringify(chatResponse, null, 2)}</pre>
        </div>
      )}
                            </div>
                    </footer>
                                
                    </div> */}
                </div>

                <ChatPage/>
</section>
    );
};

export default CreatePost;
