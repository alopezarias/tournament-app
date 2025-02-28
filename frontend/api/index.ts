import ky from 'ky';

const api = ky.create({
    prefixUrl: '/api',
    hooks: {
        beforeRequest: [
            request => {
                const token = localStorage.getItem('token');
                if (token) {
                    request.headers.set('Authorization', `Bearer ${token}`);
                }
            }
        ]
    }
});

export default api;
