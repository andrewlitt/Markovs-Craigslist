import React from 'react';
import { Dot } from 'react-animated-dots';
import { useEffect, useState } from 'react';
import './App.css';

function App() {

  const [title, setTitle] = useState(null);
  const [sentences, setSentences] = useState(null);
  async function getData() {
    const res = await fetch('/api').then(r => r.json());
    const title = res.title;
    const sentences = res.sentences;
    setTitle(title);
    setSentences(sentences);
  }

  function another() {
    setTitle(null);
    setSentences(null);
    getData();
  }
  useEffect(() => {
    getData();
  }, []);

  return (
    <main className="App">
      <h1>markovs craigslist</h1>
      <div className='posting'>
        {title ? <h2>{title}</h2> : <h2>Loading Content<Dot>.</Dot><Dot>.</Dot><Dot>.</Dot></h2>}
        <p>
          {sentences? sentences.map(sentence => {return sentence+" "}) : ''}
        </p>
      </div>
      <button onClick={another}>
        click for another
      </button>
    </main>
  );
}

export default App;
