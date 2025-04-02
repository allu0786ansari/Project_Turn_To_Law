import { useState } from "react";
import FileUpload from "../components/FileUpload";
import QnA from "../components/QnA";
import ResponseDisplay from "../components/ResponseDisplay";
import FactCheck from "../components/FactCheck";

const Home = () => {
  const [documentId, setDocumentId] = useState(null);
  const [response, setResponse] = useState("");

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Legal Document Q&A</h1>
      <FileUpload onFileUpload={setDocumentId} />
      {documentId && <QnA documentId={documentId} onResponse={setResponse} />}
      {response && <ResponseDisplay response={response} />}
      {response && <FactCheck response={response} />}
    </div>
  );
};

export default Home;
