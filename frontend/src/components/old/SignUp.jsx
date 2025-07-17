import React, { useState } from "react";
import './SignUp.css'
import { Autocomplete } from "@react-google-maps/api";


const SignUp = () => {
  const [formData, setFormData] = useState({
    name: "",
    email:"",
    age: "",
    gender: "",
    location:"",
    height: "",
    weight: "",
    dob: "",
    goal: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePlaceSelect = (place) => {
    if (place) {
      setFormData({ ...formData, location: place.formatted_address });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form Data Submitted:", formData);
  };

  return (
    <div className="SignUp">
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Sign Up</h2>
        <form onSubmit={handleSubmit} className="form">
          {/* Name */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Name:</label>
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleChange}
              className="w-2/3 p-3 h-30 border rounded-lg"
              required
            />
          </div>
          <br></br>

          <div className="flex items-center justify-between">
            <label className="w-1/3">Email:</label>
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              className="w-2/3 p-3 h-20 border rounded-lg"
              required
            />
          </div>
          <br></br>

          {/* Age */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Age:</label>
            <input
              type="number"
              name="age"
              placeholder="Age"
              value={formData.age}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            />
          </div>
          <br></br>

          {/* Gender */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Gender:</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            >
              <option value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <br></br>

          {/* Location */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Location:</label>
            <Autocomplete
              onLoad={(autocomplete) => (window.autocomplete = autocomplete)}
              onPlaceChanged={() =>
                handlePlaceSelect(window.autocomplete.getPlace())
              }
            >
              <input
                type="text"
                name="location"
                value={formData.location}
                placeholder="Search location"
                className="w-2/3 p-2 border rounded-md"
                required
              />
            </Autocomplete>
          </div>
          <br></br>

          {/* Height */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Height (cm):</label>
            <input
              type="text"
              name="height"
              placeholder="Height"
              value={formData.height}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            />
          </div>
          <br></br>

          {/* Weight */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Weight (kg):</label>
            <input
              type="text"
              name="weight"
              placeholder="Weight"
              value={formData.weight}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            />
          </div>
          <br></br>

          {/* DOB */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">DOB:</label>
            <input
              type="date"
              name="dob"
              value={formData.dob}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            />
          </div>
          <br></br>

          {/* User Goal */}
          <div className="flex items-center justify-between">
            <label className="w-1/3">Goal:</label>
            <select
              name="goal"
              value={formData.goal}
              onChange={handleChange}
              className="w-2/3 p-2 border rounded-md"
              required
            >
              <option value="">Select Your Goal</option>
              <option value="weight_gain">Weight Gain</option>
              <option value="diet_check">Diet Check</option>
              <option value="weight_loss">Weight Loss</option>
            </select>
          </div>
          <br></br>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200"
          >
            Sign Up
          </button>
        </form>
      </div>
    </div>
    </div>
  );
};

export default SignUp;
