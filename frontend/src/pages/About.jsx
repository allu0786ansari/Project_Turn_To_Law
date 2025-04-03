import "../styles/About.css"; // Add a CSS file for styling the About page

const About = () => {
  return (
    <div className="about-container p-4">
      <h1 className="about-title">About Smart Legal Q&A System</h1>
      <p className="about-description">
        The <strong>Smart Legal Q&A System</strong> is an AI-powered platform designed to assist users in navigating complex legal documents and queries. 
        It combines advanced natural language processing (NLP) with legal domain expertise to provide accurate and reliable answers to legal questions.
      </p>

      <h2 className="about-subtitle">Key Features</h2>
      <ul className="about-features">
        <li><strong>Document Upload:</strong> Upload legal documents (PDF, DOCX, TXT, images) and extract meaningful text for analysis.</li>
        <li><strong>Q&A:</strong> Ask questions about uploaded documents and receive AI-generated answers tailored to the document's content.</li>
        <li><strong>Fact-Checking:</strong> Validate AI-generated responses using trusted legal sources to ensure accuracy and reliability.</li>
        <li><strong>News Feed:</strong> Stay updated with the latest legal news and developments from trusted sources.</li>
        <li><strong>Summarization:</strong> Summarize lengthy legal documents for quick and easy understanding.</li>
      </ul>

      <h2 className="about-subtitle">Why Use This Platform?</h2>
      <p className="about-description">
        Legal documents can be complex and time-consuming to analyze. The Smart Legal Q&A System simplifies this process by leveraging AI to:
      </p>
      <ul className="about-benefits">
        <li>Provide quick and accurate answers to legal queries.</li>
        <li>Save time by summarizing lengthy documents.</li>
        <li>Ensure reliability through fact-checking with trusted sources.</li>
        <li>Keep users informed with the latest legal news and updates.</li>
      </ul>

      <h2 className="about-subtitle">Technology Stack</h2>
      <p className="about-description">
        The platform is built using modern technologies to ensure scalability, performance, and ease of use:
      </p>
      <ul className="about-tech-stack">
        <li><strong>Frontend:</strong> React.js with TailwindCSS for a responsive and user-friendly interface.</li>
        <li><strong>Backend:</strong> FastAPI for handling API requests and integrating AI models.</li>
        <li><strong>AI Models:</strong> GPT-based models for natural language understanding and response generation.</li>
        <li><strong>Database:</strong> Optional integration for storing user queries and document embeddings.</li>
      </ul>

      <h2 className="about-subtitle">Future Enhancements</h2>
      <p className="about-description">
        We aim to continuously improve the platform by adding features such as:
      </p>
      <ul className="about-future">
        <li>User authentication for personalized experiences.</li>
        <li>Support for additional file formats and languages.</li>
        <li>Advanced analytics for legal trends and insights.</li>
      </ul>

      <p className="about-footer">
        This project is designed to empower users with AI-driven tools for legal research and analysis. Whether you're a legal professional, a student, or someone seeking legal clarity, the Smart Legal Q&A System is here to assist you.
      </p>
    </div>
  );
};

export default About;