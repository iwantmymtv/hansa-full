import { Layout, Menu } from "antd";
import Link from "next/link";

const { Header, Content, Footer } = Layout;

export default function MainLayout({ children }) {
  const menu_items = [
    {
      key: 1,
      label: "Boltok",
      link: "/boltok",
    },
    {
      key: 2,
      label: "Vásárlások",
      link: "/vasarlasok",
    },
    {
      key: 3,
      label: "Cikkek",
      link: "/cikkek",
    },
    {
      key: 4,
      label: "Partnerek",
      link: "/partnerek",
    },
  ];
  return (
    <Layout className="layout" 
    style={{
      height:"100vh",
      display:"flex",
      flexDirection:"column",
      justifyContent:"space-between",
      alignItems:"space-between"
    }}>
      <Header>
        <div className="logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
          {menu_items.map((i) => {
            return (
              <Menu.Item key={i.key}>
                <Link href={i.link}>{i.label}</Link>
              </Menu.Item>
            );
          })}
        </Menu>
      </Header>
      <Content
        style={{
          padding: "20px 50px",
        }}
      >
        <div className="site-layout-content">{children}</div>
      </Content>
      <Footer
        style={{
          textAlign: "center",
        }}
      >
        Csá
      </Footer>
    </Layout>
  );
}
