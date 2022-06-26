import '../styles/globals.css'
import 'antd/dist/antd.css';
import MainLayout from '../components/layout'

function MyApp({ Component, pageProps }) {
  return (
    <MainLayout>
      <Component {...pageProps} />
    </MainLayout>
  )
}

export default MyApp
