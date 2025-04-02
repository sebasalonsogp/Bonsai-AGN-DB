import { useState } from "react";
import clsx from "clsx";
import { Menu, X, Database } from "lucide-react";
import NavButton from "./NavButton";


export default function Navbar() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    }
    return (<header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <nav className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
                <div className="flex items-center">
                    <div className="flex-shrink-0">
                        <div className="flex items-center gap-2">
                            <Database size={22} className="text-slate-700" />
                            <span className="text-slate-800 font-medium text-lg">AGN-DB</span>
                        </div>
                    </div>
                </div>
                <div className="hidden md:block">
                    <div className="ml-10 flex items-baseline space-x-4">
                        <NavButton name="Home" route="/" />
                        <NavButton name="Search" route="search" />
                        <NavButton name="People" route="people" />
                        <NavButton name="Information" route='information' />
                    </div>
                </div>
                <div className="md:hidden">
                    <button
                        onClick={toggleMenu}
                        className="inline-flex items-center justify-center p-2 rounded-md text-slate-600 hover:text-slate-800 focus:outline-none"
                    >
                        <span className="sr-only">Open main menu</span>
                        {isMenuOpen ? (
                            <X className="block h-6 w-6" aria-hidden="true" />
                        ) : (
                            <Menu className="block h-6 w-6" aria-hidden="true" />
                        )}
                    </button>
                </div>
            </div>
        </nav>

        {/* Mobile menu */}
        <div className={clsx("md:hidden", isMenuOpen ? "block" : "hidden")}>
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-slate-200">
                <NavButton name="Home" route="/" />
                <NavButton name="Search" route="search" />
                <NavButton name="People" route="people" />
                <NavButton name="Information" route='information' />
            </div>
        </div>
    </header>)
}