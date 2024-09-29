import './Entry.css';
import Modal from './Modal';
import { useState } from 'react';

// Custom Progress component
const Progress = ({ value }) => {
    return (
        <div className="progress-bar" style={{ width: '100%', backgroundColor: '#e0e0e0', borderRadius: '4px' }}>
            <div
                style={{
                    width: `${value}%`,
                    backgroundColor: '#4CAF50',
                    height: '20px',
                    borderRadius: '4px',
                    transition: 'width 0.5s ease-in-out'
                }}
            />
        </div>
    );
};

export default function Entry() {
    const [open, setOpen] = useState(true);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [formData, setFormData] = useState({
        fname: '',
        lname: '',
        bmonth: '',
        byear: '',
        zipcode: ''
    });
    const [responseData, setResponseData] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setProgress(0);

        const simulateProgress = () => {
            setProgress(prevProgress => {
                if (prevProgress >= 90) {
                    return prevProgress;
                }
                return prevProgress + 10;
            });
        };

        const progressInterval = setInterval(simulateProgress, 500);

        try {
            const response = await fetch('http://127.0.0.1:8000/user_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: formData.fname,
                    last_name: formData.lname,
                    birth_month: formData.bmonth,
                    birth_year: formData.byear,
                    zipcode: formData.zipcode
                }),
            });
            const data = await response.json();
            console.log('Success:', data);
            setResponseData(data);
            setProgress(100);
            setTimeout(() => {
                setOpen(false);
                setLoading(false);
            }, 500);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
            // Handle errors (e.g., show an error message)
        } finally {
            clearInterval(progressInterval);
        }
    };

    const renderResponseData = () => {
        if (!responseData) return null;
        
        return (
            <div className="response-data">
                <h2>Your Voter Information</h2>
                {Object.entries(responseData).map(([key, value]) => (
                    <p key={key}><strong>{key}:</strong> {value}</p>
                ))}
            </div>
        );
    };

    return (
        <div className='flexbox'>
            <div className='header'>
                <div className='logo'>
                </div>
            </div>
            {open ? (
                <Modal open={open} classname='mymodal'>
                    <div className='entrymodal'>
                        {loading ? (
                            <div className="loading-container">
                                <p>Loading...</p>
                                <Progress value={progress} className="w-full" />
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit}>
                                <div className='logo'></div>
                                <p>Search for your voter information</p>
                                <label htmlFor="fname">First name: </label>
                                <input type="text" id="fname" name="fname" value={formData.fname} onChange={handleInputChange} /><br /><br />
                                <label htmlFor="lname">Last name: </label>
                                <input type="text" id="lname" name="lname" value={formData.lname} onChange={handleInputChange} /><br /><br />
                                <label htmlFor="bmonth">Birth month: </label>
                                <input type="text" id="bmonth" name="bmonth" value={formData.bmonth} onChange={handleInputChange} /><br /><br />
                                <label htmlFor="byear">Birth year: </label>
                                <input type="text" id="byear" name="byear" value={formData.byear} onChange={handleInputChange} /><br /><br />
                                <label htmlFor="zipcode">ZIP code: </label>
                                <input type="text" id="zipcode" name="zipcode" value={formData.zipcode} onChange={handleInputChange} /><br /><br />
                                <input type="submit" value="Submit" />
                            </form>
                        )}
                    </div>
                </Modal>
            ) : (
                renderResponseData()
            )}
        </div>
    );
}