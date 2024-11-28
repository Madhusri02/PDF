import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

function Header() {

  const navigate = useNavigate();


  const headerVarient = {
    hidden:{
      top:-100
    },
    visible:{
      top:2,
      transition:{
        type:"spring",
        damping:10
      }
    }
  }
  return (
    <>
      <motion.div variants={headerVarient} initial="hidden" animate="visible" className=" w-[95%] overflow-x-hidden absolute flex flex-col justify-center items-center  bg-transparent">
        <div className='flex justify-between w-full'>
        <h1 className="self-start ml-10 my-5 font-bold text-[2.5vh] text-[#a17fe0]">DREAM PDF</h1>
        <button className='h-fit w-[5%] p-2 mt-4 bg-[#59C173] rounded-lg text-white ' onClick={(e) => navigate('/chat')}>article</button>
        </div>
        
        <hr className=" w-[95%] border-t-2 border-[#59C173]" />
      
      </motion.div>
    </>
  );
}

export default Header;
