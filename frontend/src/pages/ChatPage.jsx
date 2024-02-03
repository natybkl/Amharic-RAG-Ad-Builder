
import  { useEffect, useRef, useState } from 'react';
import '../App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
// import PdfTextExtract from './PdfTextExtract';
import axios from 'axios';

// const API_KEY =  import.meta.env.VITE_REACT_APP_CHATGPT_API_KEY;


const ChatPage = (props) => {
  const fileInputRef = useRef(null);
  const [text, setText] = useState('');
  const [prompt, setPrompt] = useState('');

  // console.log("selectedModel chat page: ", props.selectedModel)

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



 
  // useEffect(() => {
  //   if(text){
  //     setPrompt(`
  //     Answer the following question based on the information in the provided text:
  //     ${text}
  //     `)
  //   }
  //   else{
  //     setPrompt("")
  //   }
  // }, [text]);

  const handleButtonClick = () => {
    // Trigger the file input when the button is clicked
    fileInputRef.current.click();
  };



  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];

    const formData = new FormData();
    formData.append('file', selectedFile);


    try {
      const response = await axios.post('http://127.0.0.1:5000/extract-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setText(response.data.data);
    } catch (error) {
      console.error(error);
    }

  };

  const systemMessage = { //  Explain things like you're talking to a software professional with 5 years of experience.
    "role": "system", "content": prompt
  }
  


  const [messages, setMessages] = useState([
  
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (message) => {
    const newMessage = {
      message,
      direction: 'outgoing',
      sender: "user"
    };

    const newMessages = [...messages, newMessage];
    
    setMessages(newMessages);

    // Initial system message to determine ChatGPT functionality
    // How it responds, how it talks, etc.
    setIsTyping(true);
    await processMessageToChatGPT(newMessages);
  };

  async function processMessageToChatGPT(chatMessages) { // messages is an array of messages
    // Format messages for chatGPT API
    // API is expecting objects in format of { role: "user" or "assistant", "content": "message here"}
    // So we need to reformat

    console.log("called 1")

    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant";
      } else {
        role = "user";
      }
      return { role: role, content: messageObject.message}
    });


  
    const apiRequestBody = {
      "model": "gpt-4-1106-preview",
      "messages": [
        systemMessage,  // The system message DEFINES the logic of our chatGPT
        ...apiMessages // The messages from our chat with ChatGPT
      ]
    }

    console.log("called 2")



        try {
          const model_type = "gpt-4-1106-preview"
          // console.log("model", selectedModel);
          console.log("called 3")
          console.log(apiRequestBody.messages[apiRequestBody.messages.length-1].content)

          const response = await axios.post('https://9bba-196-189-127-38.ngrok-free.app/api/v1/chat', { message:apiRequestBody.messages[apiRequestBody.messages.length-1].content, model_type: model_type});
          // console.log(response);
          setMessages([...chatMessages, {
                message: response.data.data,
                sender: "ChatGPT"
              }]);
              setIsTyping(false);
  
        } catch (error) {
          console.error('Error fetching data:', error);
        }
  }

  return (
    <div>
    <div>
    <ChatContainer style={{ marginTop:'100px', overflow:"auto" }} > 
       <MessageList 
       
              scrollBehavior="smooth" 
              typingIndicator={isTyping ? <TypingIndicator content="Adbar is typing" /> : null}
            >
              {messages.map((message, i) => {
                return <Message style={{textAlign:'left'}} key={i} model={message} />
              })}
            </MessageList>
            </ChatContainer>
    </div>
    <div style={{position:'absolute', bottom:'20px', width:'80%', left:"0", right:"0", margin:'auto', paddingLeft:'150px'}}>

        <MessageInput
            onSend={handleSend} 
              style={{ textAlign:"left" }}  
              placeholder="Type message here" 
             />    
            
    </div>
    </div>

    // <div className="App" style={{height:"90vh", margin:'auto'}}>
    //   <div style={{ position:"relative", height: "100%", width: "700px",margin:'auto', }}>
  
    //     <MainContainer style={{padding:"10px 5px", borderRadius:'10px',
    //   display:"flex", alignItems:'center', justifyContent:'center', margin:"auto" }}>
    //       <ChatContainer >       
    //         <MessageList 
    //           scrollBehavior="smooth" 
    //           typingIndicator={isTyping ? <TypingIndicator content="ChatGPT is typing" /> : null}
    //         >
    //           {messages.map((message, i) => {
    //             return <Message style={{textAlign:'left'}} key={i} model={message} />
    //           })}
    //         </MessageList>
    //         <MessageInput
    //         onSend={handleSend} 
    //           style={{ textAlign:"left" }}  
    //           placeholder="Type message here" 
    //          />    
            
    
    //       </ChatContainer>
    //     </MainContainer>
    //   </div>
    // </div>
  )
}

export default ChatPage