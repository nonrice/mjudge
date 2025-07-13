import { useEffect, useState } from 'react';

export default function CountdownTimer({ timingData, offset }) {
    const endTimeUTC = new Date(timingData.end_time);
    const [remaining, setRemaining] = useState(-1);

    useEffect(() => {
        if (offset === undefined) return; // wait for offset to be ready

        const update = () => {
            const now = Date.now() + offset;
            setRemaining(Math.max(0, Math.floor(endTimeUTC.getTime() - now)));
        };

        update();
        const interval = setInterval(update, 1000);
        return () => clearInterval(interval);
    }, [endTimeUTC, offset]);

    if (remaining < 0) return <span>Loading...</span>;
    if (remaining === 0) return <span>Completed</span>;

    const seconds = Math.floor((remaining / 1000) % 60);
    const minutes = Math.floor((remaining / 1000 / 60) % 60);
    const hours = Math.floor((remaining / 1000 / 60 / 60));
    const formatTime = (h, m, s) =>
        `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

    return (
        <span>
            {formatTime(hours, minutes, seconds)}
            <span style={{ color: 'gray' }}> (Offset: {offset} ms)</span>
        </span>
    );
}
