import axios from 'axios';

const api = axios.create({
    "baseURL": "https://reliability-django.herokuapp.com"
});

class ReabilityService {
    async generateReport( url, mustHaveLabels, mustNotHaveLabels ){
        const body = {
            "url": url,
            "must_have_labels": mustHaveLabels,
            "must_not_have_labels": mustNotHaveLabels,
            "github_token": []
        };
        const report = await api.post('/repository', body);
        console.log(report.data);
        return report.data;
    }
}

const reabilityService = new ReabilityService();
export default reabilityService;
