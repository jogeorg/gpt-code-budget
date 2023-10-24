import AssistantIcon from "@mui/icons-material/Assistant";

import "./Sidebar.css";

export default function Sidebar(props: {
  models: Array<{ name: string; displayName: string }>;
  setModels: any;
  selectedModel: string;
  onSelectModel: any;
  setOpenAIKey: any;
  openAIKey: string;
  openAIApiBase: string;
  setopenAIApiBase: any;
  openAIApiVersion: string;
  setopenAIApiVersion: any;
}) {
  const handleOpenAIButtonClick = () => {
    const key = prompt("Please enter your Azure OpenAI key", props.openAIKey);
    if (key != null) {
      props.setOpenAIKey(key);
    }
  };
  const handleopenAIApiBaseClick = () => {
    const key = prompt(
      "Please enter your Azure OpenAI base URL",
      props.openAIApiBase
    );
    if (key != null) {
      props.setopenAIApiBase(key);
    }
  };
  const handleopenAIApiVersionClick = () => {
    const key = prompt(
      "Please enter your Azure API version",
      props.openAIApiVersion
    );
    if (key != null) {
      props.setopenAIApiVersion(key);
    }
  };
  const handleopenAIModelsClick = () => {
    const model35Name = prompt(
      "Please enter the Azure GPT3.5 Deployment Name",
      ""
    );
    const model4Name = prompt(
      "Please enter the Azure GPT4 Deployment Name",
      ""
    );

    if (model35Name !== null || model4Name !== null) {
      // Create new model objects with the entered names
      const updatedModels = [...props.models];

      if (model35Name) {
        updatedModels.push({
          name: model35Name,
          displayName: model35Name,
        });
      }

      if (model4Name) {
        updatedModels.push({
          name: model4Name,
          displayName: model4Name,
        });
      }

      // Update the models state with the updated array
      props.setModels(updatedModels);
    }
  };
  return (
    <>
      <div className="sidebar">
        <div className="logo">
          <AssistantIcon /> AOAI Code<br></br>Interpreter
          <div className="github">
            <a href="https://github.com/jogeorg/gpt-code-budget">
              Open Source - v{import.meta.env.VITE_APP_VERSION}
            </a>
          </div>
        </div>
        <div className="settings">
          <label className="header">Settings</label>
          <label>Model</label>
          <select
            value={props.selectedModel}
            onChange={(event) => props.onSelectModel(event.target.value)}
          >
            {props.models.map((model, index) => {
              return (
                <option key={index} value={model.name}>
                  {model.displayName}
                </option>
              );
            })}
          </select>
          <button onClick={handleopenAIApiBaseClick}>
            Set Azure OpenAI base URL
          </button>
          <button onClick={handleopenAIApiVersionClick}>
            Set Azure OpenAI API version
          </button>
          <button onClick={handleopenAIModelsClick}>
            Set Azure OpenAI API Deployment Names
          </button>
          <label>Credentials</label>
          <button onClick={handleOpenAIButtonClick}>
            Set Azure OpenAI key
          </button>
        </div>
      </div>
    </>
  );
}
