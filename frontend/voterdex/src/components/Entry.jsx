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
                        <label htmlFor="fname">First name:</label>
                        <input type="text" id="fname" name="fname" /><br /><br />
                        <label htmlFor="lname">Last name:</label>
                        <input type="text" id="lname" name="lname" /><br /><br />
                        <input type="submit" value="Submit" />
                    </form>
                </div>
            </Modal>
        </div>
    );
}