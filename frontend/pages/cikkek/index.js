import Head from 'next/head'
import Link from "next/link";
import AddBoltForm from './create'; 
import { DownloadOutlined,DeleteOutlined,PlusCircleOutlined } from '@ant-design/icons';
import {Table,Spin,Input,Button,Popconfirm,Modal } from 'antd';
import {useState,useEffect } from 'react';

const { Search } = Input;


export default function Cikkek() {
  const baseApiURL = 'http://localhost:8000/api/v1/cikkek/'
  const [data, setData] = useState(null)
  const [search, setSearch] = useState('')
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState([])


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
    const filter =   params.mennyisegiegyseg ? params.mennyisegiegyseg.join(',') : '' 
    
    if (params.sortOrder) {
      ordering = `${params.sortOrder==='ascend' ? '-' : ''}${params.sortField}` 
    }

    console.log(params.mennyisegiegyseg)
    setLoading(true);
    fetch(`${baseApiURL}?limit=${params.pagination.pageSize}&offset=${params.pagination.offset}&ordering=${ordering}&search=${search_param}&mennyisegiegyseg=${filter}`)
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
        if (params.mennyisegiegyseg){
          setFilters(params.mennyisegiegyseg.join(','))
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
        pageSizeOptions: [5,10,25,50,100],
        offset: 0,
        showSizeChanger: true,
      },
      search:searchTerm
    });
  }

  
  const onDownload = () => {
    document.location.href = `${baseApiURL}export?search=${search}`
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

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleModalCancel = () => {
    setIsModalVisible(false);
  };


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
    },
    {
      title: 'Cikkszám',
      dataIndex: 'cikkszam',
      key: 'cikkszam',
      sorter:true,
    },
    {
      title: 'Vonalkód',
      dataIndex: 'vonalkod',
      key: 'vonalkod',
      sorter:true,
    },
    {
      title: 'Nettó egységár',
      dataIndex: 'nettoegysegar',
      key: 'nettoegysegar',
      sorter:true,
    },
    {
      title: 'Mennyiségi egység',
      dataIndex: 'mennyisegiegyseg',
      key: 'mennyisegiegyseg',
      sorter:true,
      filters: [
        {
          text: 'Méter',
          value: 'm',
        },
        {
          text: 'Darab',
          value: 'db',
        }
      ]
    },
    {
      title: 'Verzió',
      dataIndex: 'verzio',
      key: 'verzio',
      sorter:true,
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
          <Link href={`cikkek/${record.id}`}>
            <Button type="primary" size="small">Részletek</Button>
          </Link>
          <Popconfirm cancelText="Mégse" title="Biztos kitörlöd?" onConfirm={() => handleDelete(record.id)}>
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
        <title>Cikkek</title>
        <meta name="description" content="Cikkek" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main style={{marginTop:"20px"}}>
        <div style={{marginBottom:"20px",width:"100%", textAlign:"center"}}>
        <Button onClick={showModal} type="default"  size="large" icon={<PlusCircleOutlined />} >
          Új cikk hozzáadása
        </Button>
        </div>
   
        <div style={{display:"flex"}}>
        <Search placeholder="Keresés" onSearch={onSearch} enterButton />
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


      <Modal  title="Új cikk hozzáadás" visible={isModalVisible} footer={null} onCancel={handleModalCancel}>
      <AddBoltForm/>
      </Modal>

      </main>
    </div>
  )
}
