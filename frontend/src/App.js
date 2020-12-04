import React, { useState, useRef } from 'react';
import './App.css';
import BackArrow from './back_arrow.svg';
import reabilityService from './api';

import { Line, Circle } from 'rc-progress';

const App = () => {
  const [progress, setProgress] = useState(0);
  const [color, setColor] = useState('#FF0000');
  const [loading, setLoading] = useState(false);
  let i;
  const getColor = () => {
      if(progress < 25)
        return '#FF0000';
      else if(progress < 75)
        return '#FFF000';
      else
        return '#008000';
  }

  const onClick = async () => {
    
    setColor(getColor());
    await setLoading(true);
    setProgress(progress+10);
    executeScroll();
    await reabilityService.generateReport("https://github.com/vuejs/vue", ["bug"], []);
    // for(i=0; i<5; i++) {
      
    // }

  }
  
  // const delay = ms => new Promise(res => setTimeout(res, ms));
  // const delay = new Promise((resolve) => {
  //   setTimeout(() => {
  //     resolve({
  //       DeuBom: 'sim',
  //     });
  //   }, 2000);
  // });

  // const updatePercent = async () => {
  //     await delay(0);
  //     setProgress(progress+10);
  // }

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
          <button className="saved-repos"> Angular </button>
          <button className="saved-repos"> AngularJS </button>
          <button className="saved-repos"> ASP.NET Core </button>
          <button className="saved-repos"> Spring </button>
        </div>
        <p className="description-form"> ou </p>
        <p className="description-form"> Insira o link do repositório hospedado no GitHub que deseja analisar e o nome da(s) label(s) que deseja realizar a análise.  </p>
        <div className="form-repo">
          <label for="bug-labels">Link do  Repositório</label>
          <input type="text" id="repo-url" name="repo-url"/>
          <label for="bug-labels">Labels de Bug utilizadas no Repositório</label>
          <input type="text" id="bug-labels" name="bug-labels"/>
          <label for="not-bug-labels">Labels não desejadas</label>
          <input type="text" id="not-bug-labels" name="not-bug-labels"/>
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
            <img src= "https://reliability-images.s3-sa-east-1.amazonaws.com/PZKXM09MUN.png" alt="" />
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
