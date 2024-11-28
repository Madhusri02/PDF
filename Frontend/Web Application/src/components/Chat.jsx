import React, { useState } from 'react'
import axios from 'axios'
const Chat = () => {


  const [link , setLink] = useState("") 
  const [question , setQuestion] = useState(""); 
  const [answer , setAnswer] = useState("")
  console.log(link)

console.log(question)
  const handleSubmit = async () => {
    await axios.post('http://localhost:5000/article', {link , question},
        {headers: {
            'Content-Type': 'application/json',
          }}
    )
     .then(res => {
        setAnswer(res.data.answer);
       console.log(res)
     })
     .catch(err => {
       console.log(err)
     })
     
  }
  return (
    <>
    <div className='w-screen h-screen '>
        <div className='h-full w-full flex justify-center items-start '>
        <div className='flex flex-col mt-20 gap-16'>
        
        <input type='text' onChange={(e)=> setLink(e.target.value)} className='border-black border-2 p-2'></input>
        <input type='text' onChange={(e)=> setQuestion(e.target.value)} className='border-black border-2 p-2'></input>
        <button onClick={handleSubmit} className=''>submit</button>
        {answer != "" ? answer : "check your answer here"}
    </div>
        </div>

    </div>
    </>
  )
}

export default Chat