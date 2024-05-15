import React from 'react';
import Form from './components/Form';
import Result from './components/Result';

function App() {
  const [result, setResult] = React.useState(null);

  const handleResult = (data) => {
    setResult(data);
  };

  return (
    <div>
      <h1>Python Web Interface</h1>
      <Form onResult={handleResult} />
      {result && <Result data={result} />}
    </div>
  );
}

export default App;
