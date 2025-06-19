import useSWR from 'swr';
import { fetcher } from './fetcher';

export async function calcOffset() {
    const startTime = Date.now();
    const response = await fetch('http://127.0.0.1:5001/api/server_time');
    const data = await response.json();
    const endTime = Date.now();
    const duration = endTime - startTime;
    const latency = Math.floor(duration / 2);
    const serverTime = Date.parse(data.now);

    console.log("Server time:", serverTime);
    console.log("Start time:", startTime);
    console.log("End time:", endTime);
    const time_diff = serverTime - endTime;

    console.log("Time difference:", time_diff, "ms");
    console.log("Latency:", latency, "ms");

    const total_offset = time_diff - latency;
    console.log("Calculated offset:", total_offset, "ms");
    return total_offset;
}
