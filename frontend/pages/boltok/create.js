import { Button, Select, Form, Input, Spin,Alert } from "antd";
import { useState, useEffect } from "react";

const AddBoltForm = () => {
  const [partners, setPartners] = useState(null);
  const [uploaded,setUploaded] = useState(false)
  const [loading, setLoading] = useState(false);
  const [errs, setErrors] = useState(null);

  const fetchPartners = () => {
    setLoading(true);

    fetch("http://localhost:8000/api/v1/partnerek/")
      .then((res) => res.json())
      .then((data) => {
        setPartners(data);
        setLoading(false);
      })
      .catch((error) => console.log(error));
  };

  const onFinish = (values) => {
    console.log(values)
    setLoading(true);

    fetch("http://localhost:8000/api/v1/boltok/", {
      method: "POST", 
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(values),
    })
      .then((res) => {
        if (res.ok) {
          console.log("HTTP request successful");
          setUploaded(true)
        } else {
          setUploaded(false)
        }
        return res;
      })
      .then((res) => res.json())
      .then((data) => {
        if (!uploaded){
          setErrors(data)
        }
        setLoading(false);
      })
      .catch((error) => console.log("error",error));
  };

  useEffect(() => {
    fetchPartners();
  }, []);

  const onClose = (e) => {
    setUploaded(false)
  };

  if (!partners) {
    return (
      <div
        style={{
          marginTop: "50px",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Spin />
      </div>
    );
  }

  return (
    <>
    {uploaded ? <Alert message="Hozzáasdva" closable onClose={onClose} type="success" /> :
    <Form
      name="add_new_shop"
      initialValues={{
        remember: true,
      }}
      onFinish={onFinish}
    >
      <Form.Item
        name="nev"
        rules={[
          {
            required: true,
            message: "Add meg a bolt nevét",
          },
        ]}
      >
        <Input placeholder="Bolt neve" />
      </Form.Item>
      <Form.Item
        name="partner"
        rules={[
          {
            required: true,
            message: "Add meg a partnert",
          },
        ]}
      >
        <Select placeholder="Partner">
          {partners.map((p) => {
            return <Option value={p.id}>{p.nev}</Option>;
          })}
        </Select>


      </Form.Item>
 
      <Form.Item>
        <Button type="primary" htmlType="submit" className="login-form-button">
          Hozzáadás
        </Button>
      </Form.Item>
    </Form>
    }
    </>

   
  
  );
};

export default AddBoltForm;
