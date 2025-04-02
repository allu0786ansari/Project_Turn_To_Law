import { factCheck } from "../api";
import axios from 'axios';
import '../styles/FactCheck.css';

const FactCheck = ({ response }) => {
  const handleFactCheck = async () => {
    try {
      const res = await axios.post("/fact-check", { text: response });
      alert(`Fact Check Result: ${res.data.result}`);
    } catch (error) {
      console.error("Fact check failed", error);
    }
  };

  return (
    <button onClick={handleFactCheck} className="bg-red-500 text-white px-4 py-2 mt-2">
      Fact Check
    </button>
  );
};

export default FactCheck;
