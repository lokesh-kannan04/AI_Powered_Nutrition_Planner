import React, { useState } from 'react';
import axios from 'axios';

const SymptomInput = () => {
    const [symptoms, setSymptoms] = useState('');
    const [deficiencies, setDeficiencies] = useState([]);
    const [percentages, setPercentages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/api/generate-response/', {
                symptoms: symptoms
            });
            // Update state with the response data
            setDeficiencies(res.data.deficiencies);
            setPercentages(res.data.percentages);
        } catch (error) {
            console.error('Error sending symptoms to backend:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    placeholder="Enter your symptoms here..."
                    rows="4"
                    cols="50"
                />
                <br />
                <button type="submit">Submit</button>
            </form>

            {deficiencies.length > 0 && (
                <div>
                    <h3>Deficiencies and Percentages:</h3>
                    <table border="1" cellPadding="10" cellSpacing="0">
                        <thead>
                            <tr>
                                <th>Deficiency</th>
                                <th>Percentage</th>
                            </tr>
                        </thead>
                        <tbody>
                            {deficiencies.map((deficiency, index) => (
                                <tr key={index}>
                                    <td>{deficiency}</td>
                                    <td>{percentages[index]}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default SymptomInput;