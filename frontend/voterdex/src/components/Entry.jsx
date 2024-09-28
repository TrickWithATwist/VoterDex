import './Entry.css';
import Modal from './Modal';
import { useState } from 'react';




export default function Entry() {

    const [open, setOpen] = useState(true);
    const [formData, setFormData] = useState({
        fname: '',
        lname: '',
        bmonth: '',
        byear: '',
        zipcode: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/user_info', {
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
            // Handle successful submission (e.g., show a success message, close modal)
        } catch (error) {
            console.error('Error:', error);
            // Handle errors (e.g., show an error message)
        }
    };


    //const [open, setOpen] = useState(true);  // Set to true to show modal immediately

    return (
        <div className='flexbox'>
            <div className='header'>
                <div className='logo'>
                </div>
            </div>
            <Modal open={open} classname='mymodal'>
                <div className='entrymodal'>
                    <form action="/action_page.php">
                        <div className='logo'></div>
                        <p>Search for your voter information</p>
                        <label htmlFor="fname">First name: </label>
                        <input type="text" id="fname" name="fname" /><br /><br />
                        <label htmlFor="lname">Last name: </label>
                        <input type="text" id="lname" name="lname" /><br /><br />
                        <label htmlFor="lname">Birth month: </label>
                        <input type="text" id="bmonth" name="bmonth" /><br /><br />
                        <label htmlFor="lname">Birth year: </label>
                        <input type="text" id="byear" name="byear" /><br /><br />
                        <label htmlFor="lname">ZIP code: </label>
                        <input type="text" id="zipcode" name="zipcode" /><br /><br />
                        <input type="submit" value="Submit" />
                    </form>
                </div>
            </Modal>
        </div>
    );
}