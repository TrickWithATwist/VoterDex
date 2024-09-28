import './Entry.css';
import Modal from './Modal';
import { useState } from 'react';

export default function Entry() {
    const [open, setOpen] = useState(true);  // Set to true to show modal immediately

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