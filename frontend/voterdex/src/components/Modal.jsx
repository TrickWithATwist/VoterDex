import '../App.css';

export default function Modal({open, onClose, children}) {
        if (!open) return null;

        return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" >
                {children}
            </div>
        </div>
        );
}