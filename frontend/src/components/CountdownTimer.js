import { useEffect, useState } from 'react';

export default function CountdownTimer({ endTimeUTC, offsetPromise }) {
    const [remaining, setRemaining] = useState(-1);
    const [offset, setOffset] = useState(0);

    useEffect(() => {
        let interval;
    
        offsetPromise.then(resolvedOffset => {
            setOffset(resolvedOffset);
    
            // ✅ Immediately compute remaining time on first run
            const update = () => {
                const now = Date.now() + resolvedOffset;
                setRemaining(Math.max(0, Math.floor(endTimeUTC.getTime() - now)));
            };
    
            update(); // Call once right away
            interval = setInterval(update, 1000);
        });
    
        return () => clearInterval(interval);
    }, [endTimeUTC, offsetPromise]);


    if (remaining < 0) {
        return <span>Loading...</span>;
    }

    if (remaining == 0) {
        return <span>Completed</span>;
    }

    const seconds = Math.floor((remaining / 1000) % 60);
    const minutes = Math.floor((remaining / 1000 / 60) % 60);
    const hours = Math.floor((remaining / 1000 / 60 / 60));
    const formatTime = (h, m, s) => {
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    };

    const timeString = formatTime(hours, minutes, seconds);

    return (
        <span>
            {timeString}
            <span style={{ color: 'gray' }}> (Offset: {offset} ms)</span>
        </span>
    );
}