import React, { useState, useEffect } from "react";
import { Loader, FormFields, Card } from "../components";
import { Link } from "react-router-dom";
import { africa1, telegram } from "../assets/index";

const RenderCards = ({ data, title }) => {
    if (data?.length > 0) {
        return data.map((post) => <Card key={post._id} {...post} />);
    } else {
        return <h2 className="text-brand font-bold text-xl">{title}</h2>;
    }
};

const Home = () => {
    const [loading, setLoading] = useState(false);
    const [allPosts, setAllPosts] = useState([]);
    const [searchText, setSearchText] = useState("");
    const [filteredPosts, setFilteredPosts] = useState([]);
    const [searchTimeout, setSearchTimeout] = useState(null);

    useEffect(() => {
        const fetchPosts = async () => {
            setLoading(true);
            try {
                const response = await fetch(
                    "https://dalle-hn3a.onrender.com/api/v1/post",
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    }
                );

                if (response.ok) {
                    const result = await response.json();
                    setAllPosts(result.data.reverse());
                }
            } catch (err) {
                console.log(err);
            } finally {
                setLoading(false);
            }
        };
        fetchPosts();
    }, []);

    const handleSearchChange = async (e) => {
        clearTimeout(searchTimeout);
        setSearchText(e.target.value);

        setSearchTimeout(
            setTimeout(() => {
                const filteredPosts = allPosts.filter((post) =>
                    post.prompt.toLowerCase().includes(searchText.toLowerCase())
                );
                setFilteredPosts(filteredPosts);
                setLoading(false);
            }, 500)
        );
    };

    // set dynamic imgPerPage value according to screen size
    if (window.innerWidth <= 768) {
        var dynamicPerPage = 3;
    } else {
        dynamicPerPage = 6;
    }

    // implement pagination
    const [currentPage, setCurrentPage] = useState(1);
    const [postsPerPage] = useState(dynamicPerPage);
    const indexOfLastPost = currentPage * postsPerPage;
    const indexOfFirstRepo = indexOfLastPost - postsPerPage;
    const currentPosts = allPosts.slice(indexOfFirstRepo, indexOfLastPost);

    const paginate = (pageNumber) => {
        setCurrentPage(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    // calculate page numbers
    const pageNumbers = [];
    for (let i = 1; i <= Math.ceil(allPosts.length / postsPerPage); i++) {
        pageNumbers.push(i);
    }

    return (
        <section className="mx-auto">
            <div className="md:grid md:grid-cols-2 md:grid-flow-row md:gap-4 max-w-7xl mt-16 sm:p-8 px-4 py-8 m-auto bg-white">
                <div className="hero__text grid-col-1 flex flex-col"> <br />
                    <h1 className="text-text text-blue-800">አድባር</h1>
                    <p className="mt-2 text-text max-w-[520px] text-hero text-[15px]">
                    Welcome to AIQEM, where innovation meets impact in the heart of African technology! 🌍
                    Unleashing the power of AI and Blockchain, AIQEM proudly presents አድባር – our groundbreaking Telegram Ad solution tailored for Ethiopian businesses.
                    Elevate your advertising strategy with አድባር, our end-to-end AI-based platform designed to optimize ad placements across diverse Telegram channels.
                    Explore the future of marketing with AIQEM's Amharic RAG pipeline, revolutionizing the creation of engaging Amharic text Ad content for unparalleled campaign success.
                    Join us on the forefront of technological innovation as we reshape the landscape of AI and Blockchain solutions for Ethiopian and African businesses. 🚀    
                    </p>
                    <br />
                    <Link
                        to="/create"
                        className="font-inter font-bold bg-blue-800 text-white px-2 py-1 rounded-md w-[60px]"
                    >
                        Chat
                    </Link>
                </div>
            <div className="mt-16]">
                <img src={telegram} style={{ width: 500, height: 400 }} alt="img" className=""/>
            </div>
            </div>
        </section>
    );
};

export default Home;
