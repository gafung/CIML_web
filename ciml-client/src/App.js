import React, { Component } from 'react';
import './App.css';
import Axios from 'axios';
import {Layout, Card, Row, Col, Table, Icon, Form, Select, InputNumber, Button} from 'antd';
const {Header, Content} = Layout;
const FormItem = Form.Item;
const Option = Select.Option;

// const URL = 'http://localhost:5000/';
const URL = window.location.origin;
const outputColumns = [
  {
    title: 'Model',
    dataIndex: 'model',
  },
  {
    title: 'Result',
    dataIndex: 'result',
    render: res => (res==="Y") ? <Icon style={{color: 'green'}} type="check" />: <Icon style={{color: 'red'}} type="close" />,
  }
];

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingTestData: false,
      loadingOutput: false,
      outputData: [],
      requestedModels: [
        {id: 1, name: 'KNN', k: 1, kernal: "linear"},
        {id: 2, name: 'KNN', k: 37, kernal: "linear"},
        {id: 3, name: 'DNN', k: 37, kernal: "linear"},
        {id: 4, name: 'SVM', k: 37, kernal: "linear"},
      ],
      'side': "Buy",
      'return_t5': 0.1, 
      "return_t30": 0.2, 
      "vol_sh_out_pct": 0.00008, 
      "stake_pct_chg": 0.05,
      "tran_value": 0.00003,
      "mkt_cap": 0.004,
      "prev_tran_num": 0.02,
      "hit_rate_5d": 0.4,
      "hit_rate_30d": 0.6,
      "hit_rate_90d": 0.8,
    };
  }

  createRequestedModelChangedHandler(id, field) {
    return (value) => {
      let requestedModels = this.state.requestedModels;

      const matchedIndex = this.state.requestedModels.findIndex(x=>x["id"] === id);
      requestedModels[matchedIndex][field] = value;
      this.setState({
        requestedModels: requestedModels
      });
    };
  }

  handleAddModel() {
    let requestedModels = this.state.requestedModels;
    requestedModels.push({id: new Date(), name: 'KNN', k: 1, kernal: "linear"});
    this.setState({requestedModels: requestedModels});
  }

  removeModel(id) {
    const newModels = this.state.requestedModels.filter(model=>model["id"]!==id);
    this.setState({requestedModels: newModels});
  }

  handleInputChanged_side(value) {
    this.setState({"side": value});
  }
  handleInputChanged_return_t5(value) {
    this.setState({"return_t5": value});
  }
  handleInputChanged_return_t30(value) {
    this.setState({"return_t30": value});
  }
  handleInputChanged_vol_sh_out_pct(value) {
    this.setState({"vol_sh_out_pct": value});
  }
  handleInputChanged_stake_pct_chg(value) {
    this.setState({"stake_pct_chg": value});
  }
  handleInputChanged_tran_value(value) {
    this.setState({"tran_value": value});
  }
  handleInputChanged_mkt_cap(value) {
    this.setState({"mkt_cap": value});
  }
  handleInputChanged_prev_tran_num(value) {
    this.setState({"prev_tran_num": value});
  }
  handleInputChanged_hit_rate_5d(value) {
    this.setState({"hit_rate_5d": value});
  }
  handleInputChanged_hit_rate_30d(value) {
    this.setState({"hit_rate_30d": value});
  }
  handleInputChanged_hit_rate_90d(value) {
    this.setState({"hit_rate_90d": value});
  }
  handleLoadTestData(){
    const url = URL + '/random_data';
    this.setState({loadingTestData: true}, ()=>{
      Axios.get(url).then(response=>{
        this.setState({
          loadingTestData: false,
          "side": (response.data["side"] > 0.5) ? "Buy" : "Sell",
          "return_t5": response.data["return_t5"],
          "return_t30": response.data["return_t30"],
          "vol_sh_out_pct": response.data["vol_sh_out_pct"],
          "stake_pct_chg": response.data["stake_pct_chg"],
          "tran_value": response.data["tran_value"],
          "mkt_cap": response.data["mkt_cap"],
          "prev_tran_num": response.data["prev_tran_num"],
          "hit_rate_5d": response.data["hit_rate_5d"],
          "hit_rate_30d": response.data["hit_rate_30d"],
          "hit_rate_90d": response.data["hit_rate_90d"],
        });
      });
    });
    
  }
  handleSubmit() {
    this.setState({outputData: [], loadingOutput: true}, ()=>{
      let fullUrl;
      const requestedCounts = this.state.requestedModels.length;
      let finishedRequest = 0;
      this.state.requestedModels.forEach((model, i)=>{
        if(model["name"] === "KNN") {
          fullUrl = URL + '/knn?k=' + model["k"] + "&";
        } else if (model["name"] === "SVM") {
          fullUrl = URL + '/svm?kernal=' + model["kernal"] + "&";
        } else{
          fullUrl = URL + '/dnn?';
        }
        fullUrl += ['side', 'return_t5', "return_t30", "vol_sh_out_pct", "stake_pct_chg", "tran_value", "mkt_cap",
        "prev_tran_num", "hit_rate_5d", "hit_rate_30d", "hit_rate_90d"].map(field=>field+"="+this.state[field]).join("&");
        Axios.get(fullUrl).then(response=>{
          finishedRequest += 1;
          let outputData = this.state.outputData;
          let displayName;
          if(model["name"] === "KNN"){
            displayName = `KNN (K=${model["k"]})`;
          } else if(model["name"] === "SVM"){
            displayName = `SVM (Kernal=${model["kernal"]})`;
          } else {
            displayName = "DNN";
          }
          outputData.push({
            key: i,
            model: displayName,
            result: response.data["result"],
          });
          if(finishedRequest === requestedCounts){
            this.setState({
              outputData: outputData,
              loadingOutput: false,
            });
          } else {
            this.setState({
              outputData: outputData
            });
          }
        }).catch(error=>{
          finishedRequest += 1;
          if(finishedRequest === requestedCounts){
            this.setState({
              loadingOutput: false,
            });
          }
        });
      });
    });
  }

  render() {
    const modelOptions = ["KNN", "SVM", "DNN"].map(model=>
      <Option key={model} value={model}>{model}</Option>
    );

    const forms = this.state.requestedModels.map((model, i)=>{

      let argFormItem;
      if(model["name"] === "KNN") {
        argFormItem = <FormItem label="K">
          <InputNumber defaultValue={model["k"]} min={1} onChange={this.createRequestedModelChangedHandler(model["id"], "k").bind(this)}/>
        </FormItem>;
      } else if (model["name"] === "SVM") {
        argFormItem = <FormItem label="Kernal">
          <Select defaultValue={model["kernal"]} onChange={this.createRequestedModelChangedHandler(model["id"], "kernal").bind(this)}>
            <Option value="linear">Linear</Option>
            <Option value="poly">Polynomial</Option>
            <Option value="sigmoid">Sigmoid</Option>
          </Select>
        </FormItem>;
      } else {
        argFormItem = null;
      }

      const removeModelButton = (this.state.requestedModels.length >= 2) ? <FormItem><Icon style={{cursor: "pointer"}} type="minus-circle-o" onClick={()=>this.removeModel(model["id"])}/></FormItem> : null;
        
      return (<Form layout="inline" key={i}>
        {removeModelButton}
        <FormItem label="Model">
          <Select defaultValue={model["name"]} onChange={this.createRequestedModelChangedHandler(model["id"], "name").bind(this)}>
            {modelOptions}
          </Select>
        </FormItem>
        {argFormItem}
      </Form>);
    });
    
    return (
      <div className="App">
        <Layout> 
          <Header><div style={{color: 'white'}}>COMP7404 - Insider Problem</div></Header>
          <Content>
            <Row gutter={16}>
              <Col span={8}>
                <Card title="Inputs">
                  <Form layout="inline"><FormItem label="side"><Select value={this.state["side"]} onChange={this.handleInputChanged_side.bind(this)}><Option value={"Buy"}>Buy</Option><Option value={"Sell"}>Sell</Option></Select></FormItem></Form>
                  <Form layout="inline"><FormItem label="return_t5"><InputNumber value={this.state["return_t5"]} onChange={this.handleInputChanged_return_t5.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="return_t30"><InputNumber value={this.state["return_t30"]} onChange={this.handleInputChanged_return_t30.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="vol_sh_out_pct"><InputNumber value={this.state["vol_sh_out_pct"]} onChange={this.handleInputChanged_vol_sh_out_pct.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="stake_pct_chg"><InputNumber value={this.state["stake_pct_chg"]} onChange={this.handleInputChanged_stake_pct_chg.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="tran_value"><InputNumber value={this.state["tran_value"]} onChange={this.handleInputChanged_tran_value.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="mkt_cap"><InputNumber value={this.state["mkt_cap"]} onChange={this.handleInputChanged_mkt_cap.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="prev_tran_num"><InputNumber value={this.state["prev_tran_num"]} onChange={this.handleInputChanged_prev_tran_num.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="hit_rate_5d"><InputNumber value={this.state["hit_rate_5d"]} onChange={this.handleInputChanged_hit_rate_5d.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="hit_rate_30d"><InputNumber value={this.state["hit_rate_30d"]} onChange={this.handleInputChanged_hit_rate_30d.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem label="hit_rate_90d"><InputNumber value={this.state["hit_rate_90d"]} onChange={this.handleInputChanged_hit_rate_90d.bind(this)} step={0.00001} /></FormItem></Form>
                  <Form layout="inline"><FormItem><Button type="primary" onClick={this.handleLoadTestData.bind(this)} loading={this.state.loadingTestData}>Load Test Data</Button></FormItem></Form>
                </Card>
              </Col>
              <Col span={8}>
                <Card title="Models" style={{textAlign: 'left'}}>
                  {forms}
                  <Form layout="inline"><FormItem><Button type="dashed" onClick={this.handleAddModel.bind(this)}><Icon type="plus" /> Add Model</Button></FormItem></Form>
                  <Form layout="inline"><FormItem><Button type="primary" onClick={this.handleSubmit.bind(this)} loading={this.state.loadingOutput}>Submit</Button></FormItem></Form>
                </Card>
              </Col>
              <Col span={8}>
                <Card title="Outputs">
                  <Table size="small" bordered columns={outputColumns} dataSource={this.state.outputData} pagination={false}></Table>
                </Card>
              </Col>
            </Row>
          </Content>
        </Layout>
      </div>
    );
  }
}

export default App;
