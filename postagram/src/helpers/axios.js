import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";

const axiosService = axios.create(
    {
        baseURL: "http://localhost:8000/api",
        headers: {
            "Content-Type": "application/json",
        },
    }
);

axiosService.interceptors.request.use(
    async (config) => {
        const { access } = JSON.parse(localStorage.getItem("auth"));

        config.headers.Authorization = `Bearer ${access}`;

        return config;
    }
);

axiosService.interceptors.response.use(
    (response) => Promise.resolve(response),
    (error) => Promise.reject(error),
);

const refreshAuthLogic = async (failedRequest) => {
    const { refresh } = JSON.parse(localStorage.getItem("auth"));

    return axios
        .post("/auth/refresh/", null,
            {
                baseURL: "http://localhost:8000/api",
                headers: {
                    Authorization: `Bearer ${refresh}`,
                }
            }
        )
        .then((response) => {
                const { access, refresh } = response.data;
                failedRequest.response.config.headers["Authorization"] = "Bearer" + access;
                localStorage.setItem(
                    "auth", JSON.stringify({access, refresh}),
                )
            }
        )
        .catch(() => {
                localStorage.removeItem("auth");
            }
        )
}

createAuthRefreshInterceptor(axiosService, refreshAuthLogic);s

export function fetcher(url) {
    return axiosService.get(url).then((response) => response.data);
}

export default axiosService;