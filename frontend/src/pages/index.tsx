import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const onFileUpload = async () => {
    if (!file) {
      setMessage('ファイルが選択されていません。');
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/simply-summarize-pdf', formData);
      setMessage(response.data.message);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setMessage(error.response?.data.message || '通信エラーが発生しました。');
      } else {
        setMessage('通信エラーが発生しました。');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl mb-4">PDFかんたん日本語要約</h1>
      <div className='flex flex-col'>
        <input type="file" onChange={onFileChange} className="mb-4" />
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-32"
          onClick={onFileUpload}
          disabled={isLoading}
        >
          アップロード
        </button>
      </div>

      {isLoading && (
        <div className="flex justify-center mt-4">
          <div className="animate-spin h-10 w-10 border-4 border-blue-500 rounded-full border-t-transparent"></div>
        </div>
      )}
      {message && (
        <div className="mt-4">
          <p>{message}</p>
        </div>
      )}
    </div>
  );
};

export default App;
