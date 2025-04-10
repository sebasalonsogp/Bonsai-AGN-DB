import './App.css'
import Layout from './components/layout'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Search from './pages/Search.jsx';
import People from './pages/People.jsx';
import Information from './pages/Information.jsx';

function App() {
  return (
    <Router>
        <Routes>
            {/* All routes inside Layout will share the header */}
            <Route path="/" element={<Layout />}>

                {/* Routes we need: Home, Search, People, Information */}
                <Route index element={<Home />} />
                <Route path="search" element={<Search />} />
                <Route path="people" element={<People />} />
                <Route path="information" element={<Information />} />

            </Route>
        </Routes>
    </Router>
  )
}

export default App
