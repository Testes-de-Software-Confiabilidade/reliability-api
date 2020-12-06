import React, { useState, useRef } from 'react';
import './App.css';
import BackArrow from './back_arrow.svg';
import {savedRepos} from './mock';

import { Circle } from 'rc-progress';

const App = () => {
  const [progress, setProgress] = useState(0);
  const [color, setColor] = useState('#FF0000');
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState('');
  const [bugLabels, setBugLabels] = useState('');
  const [othersLabels, setOthersLabels] = useState('');
  const [image, setImage] = useState('');
  let response;

  const getColor = () => {
      if(progress < 25)
        return '#FF0000';
      else if(progress < 75)
        return '#FFF000';
      else
        return '#008000';
  }

  const onClick = async () => {
    await setLoading(true);
    executeScroll();
    response = await reabilityService.generateReport(
      url,
       bugLabels.split(', '),
        othersLabels.split(', ')
      );
      if(response.link.includes('png')){
        await setImage(response.link);
        await updateProgressBar(100);
      }
      else{
        // implementar código de quando estiver carregando
        await updateProgressBar(10);
      }
      

  }

  const updateProgressBar = async (progress) =>{
    await setProgress(progress);
    setColor(getColor());
  }
  const buttonClickSetForm = (key) => {
    setUrl(savedRepos[key]["url"]);
    setBugLabels(savedRepos[key]["must_have_labels"]);
    setOthersLabels(savedRepos[key]["must_not_have_labels"]);
  }

  const myRef = useRef(null);

   const executeScroll = () => myRef.current.scrollIntoView();

  return (
    <div className="app">
      <div className="navbar">
        API Confiabilidade
      </div>
      <section className="main-page-body"> 
        <h1 className="main-title">Análise da Confiabilidade de Softwares de Código Aberto</h1>
        <p className="description-techs">Selecione um Framework para preencher os dados dos seguintes repositórios: </p>
        <div className="techs-list">
          <button className="saved-repos" onClick={()=>{buttonClickSetForm("angular");}}> Angular </button>
          <button className="saved-repos" onClick={()=>{buttonClickSetForm("angularjs");}}> AngularJS </button>
          <button className="saved-repos" onClick={()=>{buttonClickSetForm("aspnet");}}> ASP.NET Core </button>
          <button className="saved-repos" onClick={()=>{buttonClickSetForm("spring");}}> Spring </button>
        </div>
        <p className="description-form"> ou </p>
        <p className="description-form"> Insira o link do repositório hospedado no GitHub que deseja analisar e o nome da(s) label(s) que deseja realizar a análise.  </p>
        <div className="form-repo">
          <label for="bug-labels">Link do  Repositório</label>
          <input
            type="text"
            id="repo-url"
            name="repo-url"
            value={url}
            onChange={(e)=>setUrl(e.target.value)}
          />

          <label for="bug-labels">Labels de Bug utilizadas no Repositório</label>
          <input
            type="text"
            id="bug-labels"
            name="bug-labels"
            value={bugLabels}
            onChange={(e)=>setBugLabels(e.target.value)}
          />

          <label for="not-bug-labels">Labels não desejadas</label>
          <input
            type="text"
            id="not-bug-labels"
            name="not-bug-labels"
            value={othersLabels}
            onChange={(e)=>setOthersLabels(e.target.value)}
          />
            <button
              className="form-send-button"
              onClick={() => {
                onClick();
                }
              }> Enviar </button>
        </div>
        <img src={BackArrow} className="image-back-arrow" width="100" alt="BackArrow" />
      </section>
      {
        loading ?
      (
        <section ref={myRef} className="result-page">
        {  progress < 100 ? (
          <>
            <div>
              <Circle className="loading-bar" percent={progress} strokeWidth="4" strokeColor={color} />
            </div>
            <h2>Carregando resultado...</h2>
          </>) : (
            <img src={image} alt="" />
          )
        }
        
      </section>
    ) : 
      null
      }

    </div>
  );
}

export default App;
