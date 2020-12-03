
import './App.css';
import BackArrow from './back_arrow.svg';

const App = () => {
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
      <form className="form-repo">
        <label for="bug-labels">Link do  Repositório</label>
        <input type="text" id="repo-url" name="repo-url"/>
        <label for="bug-labels">Labels de Bug utilizadas no Repositório</label>
        <input type="text" id="bug-labels" name="bug-labels"/>
        <label for="not-bug-labels">Labels não desejadas</label>
        <input type="text" id="not-bug-labels" name="not-bug-labels"/>
        <input type="submit" value="Enviar"/>
      </form>
    <img src={BackArrow} />
      </section>
    </div>
  );
}

export default App;
