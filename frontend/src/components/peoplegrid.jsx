import React from "react";

import Jef from '/photos/JeffersonBoyd.jpg?url';
import Ch from '/photos/ChrisWu.jpg?url';
import W from '/photos/Wen.jpg?url';
import P from '/photos/APeca.JPG?url';
import D from '/photos/Dominic.png?url';
import N from '/photos/Nico.jpg?url';
import S from '/photos/Sicong.jpg?url';
import Ja from '/photos/Jack.jpg?url';
import O from '/photos/ogihara.jpg?url';
import G from '/photos/giulia.jpg?url';
import Je from '/photos/jerry.png?url';
import M from '/photos/Meg_Urry.jpg?url';
import Y from '/photos/Yasmeen_Asali.jpg?url';
import A from '/photos/aritra_ghosh.JPG?url';

// Array containing details of students, including their name, title, description, and profile image
const students = [
  { name: "Jefferson Boyd", title: "Software Engineer", description: "Jefferson is an undergraduate student specializing in front-end development.", image: Jef },
  { name: "Christopher Wu", title: "Software Engineer", description: "Christopher focuses on full-stack development and data processing.", image: Ch },
  { name: "Wen Li", title: "Web Designer & Developer", description: "Wen is leading the website's front-end and back-end efforts.", image: W },
  { name: "Alessandro Peca", title: "Catalog Lead Astrophysicist", description: "Alessandro is working on AGN X-ray analysis and data classification.", image: P },
  { name: "Dominic Sicilian", title: "Catalog Implementation", description: "Dominic assists with data selection and synthesis.", image: D },
  { name: "Jerry Bonnell", title: "Lead Software Engineer", description: "Jerry leads the database development and data curation.", image: Je },
  { name: "John McKeown", title: "Machine Learning Researcher", description: "John applies ML techniques for research and data analysis.", image: Ja },
  { name: "Sicong Huang", title: "Astrophysicist Machine Learning Developer", description: "Sicong focuses on data modeling and ML applications.", image: S },
  { name: "Giulia Cerini", title: "Catalog Implementation", description: "Giulia specializes in catalog management and data classification.", image: G },
  { name: "Yasmeen Asali", title: "Machine Learning Astrophysics Tools Investigator", description: "Yasmeen applies ML techniques to galaxy research.", image: Y },
  { name: "Aritra Ghosh", title: "Imaging Classification With Machine Learning", description: "Aritra is using ML to study AGN host galaxies.", image: A },
];

// Array containing details of professors, including their name, title, description, and profile image
const professors = [
  { name: "Nico Cappelluti", title: "PI", description: "Nico studies supermassive black hole formation and cosmic backgrounds.", image: N },
  { name: "Mitsunori Ogihara", title: "CO-PI", description: "Mitsunori specializes in data mining and machine learning.", image: O },
  { name: "Meg Urry", title: "CO-PI", description: "Meg's research focuses on active galaxies and black holes.", image: M },
];

const PeopleGrid = () => {
  return (
    <div className="container mx-auto p-6">
      {/* Title Section */}
      <h2 className="text-2xl font-bold text-center mb-6">Meet Our Team</h2>
      
      {/* Students Section */}
      <h3 className="text-xl font-semibold mb-4">Students</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
        {/* Mapping the students array to display each student's information */}
        {students.map((person, index) => (
          <div key={index} className="bg-white p-4 rounded-2xl shadow-lg text-center">
            {/* Profile Image */}
            <img src={person.image} alt={person.name} className="w-24 h-24 mx-auto rounded-full mb-4 object-cover" />
            {/* Name and Title */}
            <h3 className="text-lg font-semibold">{person.name}</h3>
            <p className="text-gray-600">{person.title}</p>
            {/* Short Description */}
            <p className="text-sm text-gray-500 mt-2">{person.description}</p>
          </div>
        ))}
      </div>

      {/* Professors Section */}
      <h3 className="text-xl font-semibold mb-4">Professors</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {/* Mapping the professors array to display each professor's information */}
        {professors.map((person, index) => (
          <div key={index} className="bg-white p-4 rounded-2xl shadow-lg text-center">
            {/* Profile Image */}
            <img src={person.image} alt={person.name} className="w-24 h-24 mx-auto rounded-full mb-4 object-cover" />
            {/* Name and Title */}
            <h3 className="text-lg font-semibold">{person.name}</h3>
            <p className="text-gray-600">{person.title}</p>
            {/* Short Description */}
            <p className="text-sm text-gray-500 mt-2">{person.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PeopleGrid;
