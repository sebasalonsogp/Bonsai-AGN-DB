import { NavLink, Link } from 'react-router-dom';

export default function NavButton(props) {
    return(
        <NavLink 
            className="px-3 py-2 text-sm font-medium transition-colors active:text-slate-800 text-slate-600 hover:text-slate-800"
            to={props.route}>
            {props.name}
        </NavLink>
    );
}