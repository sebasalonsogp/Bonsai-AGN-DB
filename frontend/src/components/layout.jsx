import { Outlet } from 'react-router-dom';
import { NavLink, Link } from 'react-router-dom';
import NavButton from './NavButton';
import Navbar from './Navbar';

function Footer() {
    return (
        <footer className="text-sm flex flex-col justify-center items-center font-light p-4 bg-slate-100">
            <p>AGN-DB is supported by the University of Miami</p>
            <p>Copyright © 2025, <a className="text-blue-500 underline" href="https://welcome.miami.edu/"> University of Miami</a></p>
        </footer>
    )

}

function Layout() {
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar/>
            <main className="flex-1 my-4">
                <Outlet />
            </main>
            <Footer />
        </div>
    );

}

export default Layout;