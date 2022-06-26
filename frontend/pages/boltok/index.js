import Head from 'next/head'
import Link from "next/link";

import { DownloadOutlined,DeleteOutlined,PlusCircleOutlined } from '@ant-design/icons';
import {Table,Spin,Input,Button,Popconfirm} from 'antd';
import {useState,useEffect } from 'react';

const { Search } = Input;


export default function Boltok() {
  const baseApiURL = 'http://localhost:8000/api/v1/boltok/'
  const [data, setData] = useState(null)
  const [search, setSearch] = useState('')

  const [loading, setLoading] = useState(false)

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
    pageSizeOptions: [5,10,25,50,100],
    offset: 0,
    showSizeChanger: true,
  });

  const fetchData = (params = {}) => {
    const ordering = ''
    const search_param = params.search ? params.search : search
    
    if (params.sortOrder) {
      ordering = `${params.sortOrder==='ascend' ? '-' : ''}${params.sortField}` 
    }


    setLoading(true);
    fetch(`${baseApiURL}?limit=${params.pagination.pageSize}&offset=${params.pagination.offset}&ordering=${ordering}&search=${search_param}`)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
        setPagination({
          ...params.pagination,
          total: data.count, 
        });
        if (params.search){
          setSearch(params.search);
        }
      });
  };

  useEffect(() => {
    fetchData({
      pagination,
    });
  }, []);

  const handleTableChange = (newPagination, filters, sorter) => {
    newPagination = {
      ...newPagination,
      offset: (newPagination.current - 1) * newPagination.pageSize
    }
    fetchData({
      sortField: sorter.field,
      sortOrder: sorter.order,
      pagination: newPagination,
      ...filters,
    });
  };

  const onSearch = (searchTerm) => {
    setSearch(searchTerm)
    fetchData({
      pagination:{
        current: 1,
        pageSize: 5,
        offset:0,
      },
      search:searchTerm
    });
  }

  
  const onDownload = () => {
    document.location.href = `${baseApiURL}export?search=${search}`
  }

  const addNew = () => {
    console.log("helllllooo")
  }

  const handleDelete = (id) => {
    fetch(`${baseApiURL}${id}`, {
        method: "DELETE",
        headers: {
            'Content-type': 'application/json'
        }
    }).then(res => {
      if (res.ok) { console.log("HTTP request successful") }
      else { console.log("HTTP request unsuccessful") }
      return res
  })
  .then(res => res.json())
  .then((d) => {
    const newData = data.filter((item) => item.id !== id);
    setData(newData);
  })
  .catch(error => console.log(error))

  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      sorter:true,
      width: '10%',
    },
    {
      title: 'Név',
      dataIndex: 'nev',
      key: 'nev',
      sorter:true,
      width: '50%',
    },
    {
      title: 'Partner',
      dataIndex: 'partner_nev',
      key: 'partner',
      
    },
    {
      title: 'Egyéb',
      dataIndex: 'operation',
      width: '20%',
      render: (_, record) =>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
          <Link href={`boltok/${record.id}`}>
            <Button type="primary" size="small">Részletek</Button>
          </Link>
          <Popconfirm title="Biztos kitörlöd?" onConfirm={() => handleDelete(record.id)}>
            <DeleteOutlined/>
          </Popconfirm>
        </div>

    },
  ];

  if (!data){
    return (
      <div style={{marginTop:"50px",height:"100%",display:"flex",justifyContent:"center",alignItems:"center"}}>
        <Spin />
      </div>
    
    )
  } 

  return (
    <div >
      <Head>
        <title>Boltok</title>
        <meta name="description" content="Boltok" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main style={{marginTop:"20px"}}>
        <div style={{marginBottom:"20px",width:"100%", textAlign:"center"}}>
        <Button onClick={addNew} type="default"  size="large" icon={<PlusCircleOutlined />} >
          Új bolt hozzáadása
        </Button>
        </div>
   
        <div style={{display:"flex"}}>
        <Search placeholder="input search text" onSearch={onSearch} enterButton />
        <Button onClick={onDownload} type="dashed" icon={<DownloadOutlined />} >
          Letöltés
        </Button>
        </div>
  
       <Table 
        columns={columns} 
        pagination={pagination} 
        onChange={handleTableChange}
        loading={loading}
        dataSource={data.results} 
        style={{marginTop:"20px"}} />

      </main>
    </div>
  )
}
