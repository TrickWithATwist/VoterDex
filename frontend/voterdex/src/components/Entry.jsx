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
            <Modal open={open} class='mymodal'>
                <div className='entrymodal'>
                    <p>hi</p>
                </div>
            </Modal>
        </div>
    );
}