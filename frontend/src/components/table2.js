import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { useState, useEffect } from 'react';
import http from "../http-common";


function parseData(jsonData) {
  return Object.entries(jsonData).map(([id, data]) => ({
    id: id,
    video_file: data.video_file,
    file_type: data.file_type,
    original_name: data.original_name,
    timestamp : data.timestamp,
    status: data.status,
    _id: data.__id
  }));
}

function sortDataByTimestampDescending(data) {
  return data.sort((a, b) => {
    const timestampA = new Date(a.timestamp);
    const timestampB = new Date(b.timestamp);
    return timestampB - timestampA; // Reverse the comparison
  });
}




async function fetchData() {
  const apiUrl = '/tasks/all';

  const response = await  http.get(apiUrl).catch((error) => {
      console.error('Error fetching data:', error);
    });
    if (response)
    {
      return response.data;
    }
};

const tableDataInit = [
  {
    id: "",
  },
  // Add more objects as needed
];

function handleClick(id) {
  // Define the logic for handling the button click here
  console.log(`Button clicked for row with id ${id}`);
}

function TasksTable({refreshTable}) {

const [tableData, setTableData] = useState(tableDataInit);
const [loading, setLoading] = useState(true);

// Listen for changes in the refreshTable prop
useEffect(() => {
  async function fetchDataAndUpdateTable() {
    const data = await fetchData();
    if (data) {
      setTableData(sortDataByTimestampDescending(parseData(data)));
    }
    setLoading(false);
  }

  if (refreshTable) {
    fetchDataAndUpdateTable();
  }
}, [refreshTable]);

  // Define a custom function to fetch data


  // Call fetchData when the component mounts and whenever you want to refresh
  useEffect(() => {
    async function fetchDataAndUpdateTable() {
      const data = await fetchData();
      if (data) {
        setTableData(sortDataByTimestampDescending(parseData(data)));
      }
      setLoading(false);
    }
  
      fetchDataAndUpdateTable();
  }, []);
  
  // Empty dependency array to run it once on mount
 
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>GUID</TableCell>
            <TableCell>Тип</TableCell>
            <TableCell>Имя файла</TableCell>
            <TableCell>Загружен</TableCell>
            <TableCell>Статус</TableCell>
            <TableCell>Ид в коллекции</TableCell>
            <TableCell>Действие</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {tableData.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.video_file}</TableCell>
              <TableCell>{row.file_type}</TableCell>
              <TableCell>{row.original_name}</TableCell>
              <TableCell>{row.timestamp}</TableCell>
              <TableCell>{row.status}</TableCell>
              <TableCell>{row._id}</TableCell>
              <TableCell>
                <Button variant="contained" onClick={() => handleClick(row.id)}>Удалить</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default TasksTable;
