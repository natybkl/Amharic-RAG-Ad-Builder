import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { preview } from "../assets";
import { getRandomPrompt } from "../utils";
import { FormFields, Loader } from "../components";
import FileUpload from "../components/FileUpload";
import { telegram } from "../assets/index";

const CreatePost = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        objective: "",
        output: "HEY",
        scenario: "HEY",
    });

    const [generatingprompt, setGeneratingprompt] = useState(false);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(""); // Add this line
    

    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const handleSurpriseMe = () => {
        const randomPrompt = getRandomPrompt(form.scenario);
        setForm({ ...form, scenario: randomPrompt });
    };

    const generatePrompt = async () => {
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
  {/* Sidebar */}
                {/* <aside
                    id="sidebar"
                    className="flex flex-row w-1/4 h-full flex-shrink-0 lg:w-[240px] h-[calc(100vh-120px)] whitespace-nowrap bg-purple fixed shadow overflow-x-hidden transition-all ease-in-out"
                >
                    
                    <div className="flex flex-row">
                    <ul className="flex flex-col gap-1 mt-2 lg:mt-0">
                        <li className="text-gray-500 hover:bg-gray-100 hover:text-gray-900">
                        <a className="w-full flex items-center py-3" href="#">
                            <i className="fa-solid fa-house text-center px-5"></i>
                            <span className="whitespace-nowrap pl-1">Dashboard</span>
                        </a>
                        </li>

                        <li className="text-gray-500 hover:bg-gray-100 hover:text-gray-900">
                        <a className="w-full flex items-center py-3" href="#">
                            <i className="fa-solid fa-house text-center px-5"></i>
                            <span className="whitespace-nowrap pl-1">Dashboard</span>
                        </a>
                        </li>

                        <li className="text-gray-500 hover:bg-gray-100 hover:text-gray-900">
                        <a className="w-full flex items-center py-3" href="#">
                            <i className="fa-solid fa-chart-line text-center px-5"></i>
                            <span className="whitespace-nowrap pl-1">Reports</span>
                        </a>
                        </li>

                        <li className="text-gray-500 hover:bg-gray-100 hover:text-gray-900">
                        <a className="w-full flex items-center py-3" href="#">
                            <i className="fa-solid fa-users text-center px-5"></i>
                            <span className="whitespace-nowrap pl-1">Users</span>
                        </a>
                        </li>
                    </ul>
                    </div>
                </aside> */}
                <div className="flex flex-col w-1/3 h-full flex-shrink-0 lg:w-[240px] h-[calc(100vh-120px)] whitespace-nowrap bg-purple fixed shadow overflow-x-hidden transition-all ease-in-out pt-2">
                    <div className="flex flex-col items-start space-y-4">
                        <label className="text-lg font-bold" id="demo-radio-buttons-group-label">
                            Model Name
                        </label>

                        <div className="flex flex-col space-y-2 pl-2">
                            <div>
                                <input type="radio" id="llama2" name="radio-buttons-group" value="Llama2 Model" className="mr-2" defaultChecked />
                                <label htmlFor="llama2" className="text-base">
                                Llama2 Model
                                </label>
                            </div>


                            <div>
                                <input type="radio" id="finetunedLlama2" name="radio-buttons-group" value="Finetuned Llama2 Model" className="mr-2" />
                                <label htmlFor="finetunedLlama2" className="text-base">
                                Finetuned Llama2 Model
                                </label>
                            </div>

                            <div>
                                <input type="radio" id="gpt35Turbo" name="radio-buttons-group" value="GPT 3.5 TURBO Model" className="mr-2" />
                                <label htmlFor="gpt35Turbo" className="text-base">
                                GPT 3.5 TURBO Model
                                </label>
                            </div>

                            <div>
                                <input type="radio" id="gpt40" name="radio-buttons-group" value="GPT 4.0 Model" className="mr-2" />
                                <label htmlFor="gpt40" className="text-base">
                                GPT 4.0 Model
                                </label>
                            </div>
                            
                        </div>
                    </div>
                </div>
  {/* Main Content */}
                <div className="flex flex-col h-full md:w-3/4 px-4 py-6 sm:w-full">
                    {/* Texts */}
                    <div className="flex flex-col ml-[530px] mt-24 font-extrabold text-text text-[42px]">
                        <h1 className="md:ml-[96px] text-blue-800">አድባር</h1>
                        <p className="md:text-[36px] text-blue-800">Generate Telegram Ad</p>
                        <img src={ telegram } alt="img" className="rounded"/>
                    </div>

                    <div className="flex flex-col ml-32 w-3/4">

                        <footer className="flex-row-2 mt-2 mb-2 border-blue-800 p-4 absolute bottom-0 ml-36 w-3/4" onSubmit={handleSubmit}>
                        <label for="chat" class="sr-only">Your message</label>
                            <div class="flex items-center py-2 px-3 bg-blue-800 rounded-lg dark:bg-blue-800">
                            <FileUpload/>
                            <textarea 
                                    id="chat" 
                                    rows="1" 
                                    value={form.objective}
                                    onChange={handleChange}
                                    class="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border focus:ring-blue-500 focus:border-blue-500 dark:bg-white-800 dark:border-blue-800 dark:placeholder-blue-800 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Your message..."></textarea>
                            <button type="submit" onClick={generatePrompt} class="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600">
                                    <svg class="w-6 h-6 rotate-90" fill="white" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path></svg>
                            </button>
                            </div>
                    </footer>
                                
                    </div>
                </div>
</section>
    );
};

export default CreatePost;
