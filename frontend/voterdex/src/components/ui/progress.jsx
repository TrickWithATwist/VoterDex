// Custom Progress component
export const Progress = ({ value }) => {
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