import { useEffect, useState } from 'react';

export default function CountdownTimer({ endTimeUTC, offsetPromise }) {
    const [remaining, setRemaining] = useState(-1);
    const [offset, setOffset] = useState(0);

    useEffect(() => {
        offsetPromise.then(resolvedOffset => {
            setOffset(resolvedOffset);

            const interval = setInterval(() => {
                const now = Date.now() + resolvedOffset;

                console.log("Current time (now):", now, "Offset:", resolvedOffset, "End time:", endTimeUTC.getTime());

                setRemaining(Math.max(0, Math.floor(endTimeUTC.getTime() - now)));
            }, 1000);

            return () => clearInterval(interval);
        });
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

    return (
        <span>
            {hours}:{minutes}:{seconds}
        </span>
    );
}