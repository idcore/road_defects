import React, { Component } from "react";
import UploadService from "../services/upload-files.service";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';


export default class UploadFiles extends Component {
  constructor(props) {
    super(props);
    this.selectFiles = this.selectFiles.bind(this);
    this.upload = this.upload.bind(this);
    this.uploadFiles = this.uploadFiles.bind(this);

    this.state = {
      selectedFiles: undefined,
      progressInfos: [],
      message: []
    };
  }


  selectFiles(event) {
    this.setState({
      progressInfos: [],
      selectedFiles: event.target.files,
    });
  }

  upload(idx, file) {
    let _progressInfos = [...this.state.progressInfos];

    UploadService.upload(file, (event) => {
      _progressInfos[idx].percentage = Math.round((100 * event.loaded) / event.total);
      this.setState({
        _progressInfos,
      });
    })
      .then((response) => {
        this.setState((prev) => {
          let nextMessage = [...prev.message, "Файл загружен: " + file.name];
          return {
            message: nextMessage
          };
          
        });
        this.props.onUploadComplete(/* pass any relevant data here */);  
        return {}
      })
      .catch(() => {
        _progressInfos[idx].percentage = 0;
        this.setState((prev) => {
          let nextMessage = [...prev.message, "Не удалось загрузить файл: " + file.name];
          return {
            progressInfos: _progressInfos,
            message: nextMessage
          };
        });
      });
  }

  uploadFiles() {
    const selectedFiles = this.state.selectedFiles;

    let _progressInfos = [];

    for (let i = 0; i < selectedFiles.length; i++) {
      _progressInfos.push({ percentage: 0, fileName: selectedFiles[i].name });
    }

    this.setState(
      {
        progressInfos: _progressInfos,
        message: [],
      },
      () => {
        for (let i = 0; i < selectedFiles.length; i++) {
          this.upload(i, selectedFiles[i]);
        }
      }
    );
  }

  render() {
    const { selectedFiles, progressInfos, message} = this.state;

    return (
        <Container>
        <Row xs={2} md={2} lg={2} xl={2}>  

      <div className="file-upload-multiple">
        {progressInfos &&
          progressInfos.map((progressInfo, index) => (
                    <Col>
                        <div className="mb-2" key={index}>
                        <div>{progressInfo.fileName}</div>
                    
                    
                        <div className="progress">
                            <div
                            className="progress-bar progress-bar-info"
                            role="progressbar"
                            aria-valuenow={progressInfo.percentage}
                            aria-valuemin="0"
                            aria-valuemax="100"
                            style={{ width: progressInfo.percentage + "%" }}
                            >
                            {progressInfo.percentage}%
                            </div>
                        </div>
                        </div>
                        </Col>
          ))}
        <Col>
        <div className="row my-3">
          <div className="col-8">
            <label className="btn btn-default p-0">
              <input type="file" multiple onChange={this.selectFiles} />
            </label>
          </div>

          <div className="col-4">
            <button
              className="btn btn-success btn-sm"
              disabled={!selectedFiles}
              onClick={this.uploadFiles}
            >
              Загрузить
            </button>
          </div>
        </div>
        </Col>
        <Col>
        {message.length > 0 && (
            <ul>
              {message.map((item, i) => {
                return <li key={i}>{item}</li>;
              })}
            </ul>
        )}
        </Col>

       
      </div>
     </Row>
     </Container>

    );
  }
}