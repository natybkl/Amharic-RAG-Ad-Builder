import React from 'react'
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom'
import { aiqem_logo } from "./assets"
import { Home, CreatePost } from "./pages"
import ChatPage from './pages/ChatPage'


const App = () => {
  return (
    <BrowserRouter>
      <header className="w-full fixed flex justify-between items-center bg-blue-800 sm:px-8 px-4 py-4 border-b border-blue-800">
        <Link to="/">
          <img src={aiqem_logo} alt="Logo" /> 
        </Link>
        <Link to="/" className="font-inter font-medium text-white px-2 ml-auto">Home</Link>
        <Link to="/create" className="font-inter font-bold bg-blue-800 text-white px-2 py-1 rounded-md">Chat</Link>
      </header>
      <main className="py-8 w-full bg-white  min-h-[calc(100vh)]">
        <Routes>
          <Route path="/create" element={<CreatePost />} />
          <Route path="/" element={<Home />} />
          {/* <Route path="/chat" element={<ChatPage />} /> */}

        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App

//106e75